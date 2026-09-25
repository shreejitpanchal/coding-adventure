<#
Developer task runner (PowerShell 5.1+). Mirrors scripts/dev.sh exactly -- keep
both in sync when a gate changes, and keep them in step with .github/workflows/ci.yml.

Usage: .\scripts\dev.ps1 <task> [<task> ...]

Tasks:
  lint     ruff check (style/errors only; the rule set lives in pyproject.toml)
  test     full pytest suite
  cov      pytest under coverage -> scripts\logs\htmlcov\ + printed total
  content  content-lint tests only (fast check after editing YAML)
  all      lint test cov
  help     this text

Every task truncates scripts\logs\<task>.log, then writes its output there.
Correctness gates (lint/test/cov) are fatal: the first failure stops the run.
#>
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Tasks)

$ErrorActionPreference = "Continue"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$LogDir = Join-Path $ScriptDir "logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
Set-Location $RepoRoot

$env:NO_COLOR = "1"
$env:PYTHONUTF8 = "1"

if (Test-Path ".venv\Scripts\python.exe") { $Py = ".venv\Scripts\python.exe" }
elseif (Test-Path ".venv/bin/python") { $Py = ".venv/bin/python" }
elseif ($env:PYTHON) { $Py = $env:PYTHON }
else { $Py = "python" }

function Step($msg) { Write-Host "==> $msg" -ForegroundColor Cyan }
function Ok($msg)   { Write-Host "  ok: $msg" -ForegroundColor Green }
function Warn($msg) { Write-Host "warn: $msg" -ForegroundColor Yellow }
function Die($msg)  { Write-Host "fail: $msg" -ForegroundColor Red; exit 1 }

# Invoke-Logged <task> <exe> <args...>: capture once, strip ANSI, write once (UTF-8),
# echo to console, return the native exit code.
function Invoke-Logged {
    param([string]$Task, [string]$Exe, [string[]]$Arguments)
    $log = Join-Path $LogDir "$Task.log"
    $header = @(
        "== $Task  $((Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'))",
        "== cwd: $RepoRoot",
        "== cmd: $Exe $($Arguments -join ' ')"
    ) -join "`r`n"
    $out = (& $Exe @Arguments 2>&1 | ForEach-Object { "$_" } | Out-String -Width 4096)
    $code = $LASTEXITCODE
    $clean = $out -replace "\x1b\[[0-9;]*[mGKHF]", ""
    Set-Content -Path $log -Value ($header + "`r`n" + $clean) -Encoding utf8
    Write-Host $clean
    return $code
}

function Test-Module($name) {
    & $Py -c "import $name" 2>$null | Out-Null
    return ($LASTEXITCODE -eq 0)
}

function Task-Lint {
    Step "lint (ruff)"
    if (-not (Test-Module "ruff")) { Die "ruff is not installed in the venv -- run: $Py -m pip install -r requirements-dev.txt" }
    $code = Invoke-Logged "lint" $Py @("-m", "ruff", "check", "app", "tests", "main.py", "main_web.py")
    if ($code -ne 0) { Die "lint failed (see $LogDir\lint.log)" }
    Ok "lint"
}

function Task-Test {
    Step "test (pytest)"
    $code = Invoke-Logged "test" $Py @("-m", "pytest", "tests", "-q", "-p", "no:cacheprovider")
    if ($code -ne 0) { Die "tests failed (see $LogDir\test.log)" }
    Ok "test"
}

function Task-Content {
    Step "content lint"
    $code = Invoke-Logged "content" $Py @("-m", "pytest", "tests\test_content_lint.py", "-q", "-p", "no:cacheprovider")
    if ($code -ne 0) { Die "content lint failed (see $LogDir\content.log)" }
    Ok "content"
}

function Task-Cov {
    Step "coverage"
    if (-not (Test-Module "coverage")) { Die "coverage is not installed in the venv -- run: $Py -m pip install -r requirements-dev.txt" }
    $code = Invoke-Logged "cov" $Py @("-m", "coverage", "run", "-m", "pytest", "tests", "-q", "-p", "no:cacheprovider")
    if ($code -ne 0) { Die "coverage run failed (see $LogDir\cov.log)" }
    & $Py -m coverage html -d (Join-Path $LogDir "htmlcov") | Out-Null
    $report = (& $Py -m coverage report 2>&1 | ForEach-Object { "$_" } | Out-String -Width 4096)
    Add-Content -Path (Join-Path $LogDir "cov.log") -Value $report -Encoding utf8
    Write-Host $report
    Ok "coverage report: $LogDir\htmlcov\index.html"
}

function Usage {
    Get-Content $MyInvocation.ScriptName -TotalCount 18 | Select-Object -Skip 1 | Where-Object { $_ -ne "#>" }
}

if (-not $Tasks -or $Tasks.Count -eq 0) { Usage; exit 0 }

foreach ($task in $Tasks) {
    switch ($task) {
        "lint"    { Task-Lint }
        "test"    { Task-Test }
        "cov"     { Task-Cov }
        "content" { Task-Content }
        "all"     { Task-Lint; Task-Test; Task-Cov }
        "help"    { Usage }
        "-h"      { Usage }
        "--help"  { Usage }
        default   { Die "unknown task '$task' (try: help)" }
    }
}
