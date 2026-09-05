"""Translates raw interpreter/compiler output into concise, professional
explanations. Raw text stays available on request in the UI."""
from __future__ import annotations

import re
from typing import Optional

PYTHON_FRIENDLY: dict[str, tuple[str, str]] = {
    "SyntaxError": ("Syntax error.", "Check for a missing colon, parenthesis, or quote."),
    "IndentationError": ("Indentation error.", "Python is whitespace-sensitive -- check your indent levels."),
    "TabError": ("Inconsistent tabs/spaces.", "Stick to one or the other, not both, in the same block."),
    "NameError": ("Undefined name.", "Check the spelling, or that it's assigned before use."),
    "TypeError": ("Type mismatch.", "Check the types being combined or passed to a call."),
    "AttributeError": ("Missing attribute.", "Check the object actually has that attribute/method."),
    "ZeroDivisionError": ("Division by zero.", "Guard the denominator before dividing."),
    "ImportError": ("Import failed.", "Check the module name and that it's installed."),
    "ModuleNotFoundError": ("Module not found.", "Check the module name and that it's installed."),
    "IndexError": ("Index out of range.", "Check the sequence length before indexing."),
    "KeyError": ("Key not found.", "Check the key exists, or use .get() with a default."),
    "ValueError": ("Invalid value.", "Check the value matches what's expected here."),
    "EOFError": ("Input expected but not provided.", "Fill in the input box, then run again."),
    "RecursionError": ("Recursion too deep.", "Check the base case actually stops the recursion."),
}

JAVA_FRIENDLY: dict[str, tuple[str, str]] = {
    "NullPointerException": ("Null reference.", "Check that the object isn't null before calling a method or field on it."),
    "ArrayIndexOutOfBoundsException": ("Array index out of range.", "Check the array's length before indexing into it."),
    "IndexOutOfBoundsException": ("Index out of range.", "Check the index is within bounds for this collection."),
    "ArithmeticException": ("Arithmetic error.", "Check for division by zero."),
    "ClassCastException": ("Invalid cast.", "Check the object's actual runtime type before casting it."),
    "NumberFormatException": ("Invalid number format.", "Check the string actually contains a valid number before parsing it."),
    "StackOverflowError": ("Stack overflow.", "Check the recursion has a base case that actually stops it."),
    "IllegalArgumentException": ("Illegal argument.", "Check the value passed in matches what the method expects."),
    "IllegalStateException": ("Illegal state.", "Check the object is in the right state before calling this."),
    "ConcurrentModificationException": ("Collection modified during iteration.", "Iterate over a copy, use removeIf(), or use an Iterator's own remove() instead of mutating the collection directly."),
    "UnsupportedOperationException": ("Unsupported operation.", "Check whether this collection is immutable/fixed-size before mutating it."),
    "NoSuchElementException": ("No element found.", "Check the collection/iterator actually has an element before reading it."),
}

CPP_FRIENDLY: dict[str, tuple[str, str]] = {
    "std::out_of_range": ("Out-of-range access.", "Check the index/position is valid before accessing it (e.g. compare against .size() first)."),
    "std::invalid_argument": ("Invalid argument.", "Check the value passed in is actually valid for this operation."),
    "std::length_error": ("Length error.", "Check the requested size doesn't exceed the container's max size."),
    "std::bad_alloc": ("Out of memory.", "Check you're not allocating an unreasonably large amount of memory."),
    "std::logic_error": ("Logic error.", "Check the precondition this operation assumes actually holds."),
    "std::domain_error": ("Domain error.", "Check the input is within the valid domain for this operation."),
    "std::overflow_error": ("Arithmetic overflow.", "Check the computation doesn't exceed the type's range."),
    "std::underflow_error": ("Arithmetic underflow.", "Check the computation doesn't go below the type's range."),
    "std::runtime_error": ("Runtime error.", "Check the condition the code assumes actually holds at runtime."),
    "std::bad_cast": ("Invalid cast.", "Check the object's actual type before casting it."),
    "std::bad_optional_access": ("Accessed an empty optional.", "Check the optional actually has a value (has_value()) before dereferencing it."),
    "std::bad_variant_access": ("Wrong variant alternative accessed.", "Check which alternative is actually active before accessing it."),
}

NODE_FRIENDLY: dict[str, tuple[str, str]] = {
    "TypeError": ("Type error.", "Check the value isn't null/undefined, or isn't the type this operation expects, before using it."),
    "ReferenceError": ("Undefined reference.", "Check the spelling, or that it's declared/imported before use."),
    "RangeError": ("Value out of range.", "Check the value is within the range this operation expects (e.g. recursion depth, array length)."),
    "SyntaxError": ("Syntax error.", "Check for a missing brace, parenthesis, comma, or quote."),
    "AssertionError": ("Assertion failed.", "Check the expected vs. actual value in the output below."),
    "URIError": ("Invalid URI.", "Check the string passed to encodeURI/decodeURI is actually a valid URI component."),
    "EvalError": ("Eval error.", "Check the code passed to eval() is valid."),
    "Error": ("Error thrown.", "Check the message below for what triggered it."),
}

SPRING_FRIENDLY: dict[str, tuple[str, str]] = {
    "NoSuchBeanDefinitionException": ("No matching bean found.", "Check the bean is actually registered (@Component/@Bean) and its type/qualifier matches what's being injected."),
    "NoUniqueBeanDefinitionException": ("Multiple matching beans found.", "Use @Qualifier, @Primary, or a more specific type to disambiguate which bean should be injected."),
    "BeanCreationException": ("Bean creation failed.", "Check the constructor/factory method for this bean -- a dependency it needs may itself have failed to create."),
    "UnsatisfiedDependencyException": ("Unsatisfied dependency.", "Check every constructor/field this bean depends on is itself a registered bean."),
    "BeanCurrentlyInCreationException": ("Circular dependency.", "Two or more beans depend on each other during construction -- break the cycle or use @Lazy on one side."),
    "BeanInstantiationException": ("Bean instantiation failed.", "Check the class has a usable constructor and doesn't throw during construction."),
    "BeanNotOfRequiredTypeException": ("Bean type mismatch.", "Check the bean registered under this name/type actually matches what's being injected."),
}

DEFAULT_MESSAGE = "Something went wrong while running this code."
DEFAULT_HINT = "Check the details below and try again."

_PYTHON_CODE_FRAME_RE = re.compile(r'File "<exercise>", line (\d+)')
_JAVA_LINE_RE = re.compile(r"\.java:(\d+)")
_JAVA_EXCEPTION_RE = re.compile(r'Exception in thread "\w+" (?:[\w.]+\.)?(\w+(?:Exception|Error))')
_JAVA_COMPILE_ERROR_RE = re.compile(r":\d+: error:")

_CPP_LINE_RE = re.compile(r"main\.cpp:(\d+):")
_CPP_COMPILE_ERROR_RE = re.compile(r":\d+:\d+: error:")
_CPP_EXCEPTION_RE = re.compile(r"terminate called after throwing an instance of '([\w:]+)'")
_CPP_EXCEPTION_WHAT_RE = re.compile(r"what\(\):\s*(.+)")
_CPP_CRASH_NOTE_RE = re.compile(r"\[process (?:exited with code|terminated by signal) [^:]+: ([^\]]+)\]")

_SPRING_COMPILE_ERROR_RE = re.compile(r"COMPILATION ERROR")
_SPRING_ASSERTION_RE = re.compile(r"org\.opentest4j\.AssertionFailedError")
_SPRING_ASSERTION_DETAIL_RE = re.compile(r"expected:\s*(.+?)\s*\n\s*but was:\s*(.+)")
_SPRING_EXCEPTION_RE = re.compile(r"(?:Caused by:\s*)?(?:[\w.]+\.)?(\w+(?:Exception|Error))(?::|$)", re.MULTILINE)

# Node's default uncaught-exception printer always emits the file:line
# header on its own line (no column) directly above the source excerpt --
# distinct from stack-frame lines further down, which are "file:line:col"
# and prefixed with "at ". node_engine.py sanitizes the temp file's path
# to the literal string "<exercise>" before this ever sees it.
_NODE_HEADER_LINE_RE = re.compile(r"^<exercise>:(\d+)$", re.MULTILINE)
_NODE_STACK_FRAME_RE = re.compile(r"<exercise>:(\d+):\d+")
# Matches "TypeError: message" as well as "AssertionError [ERR_ASSERTION]: message"
# (node:assert's own error class appends a bracketed error code after the type).
_NODE_ERROR_TYPE_RE = re.compile(r"^(\w+)(?:\s*\[\w+\])?: (.+)$", re.MULTILINE)


def translate_error(stderr: str, language: str = "python") -> tuple[str, str]:
    if language in ("python", "ai"):
        # "ai" runs on the exact same Python interpreter as the python
        # track (see app/execution/registry.py) -- its stderr is genuine
        # CPython traceback text, so the same friendly-message table applies.
        exc_type = _last_exception_type(stderr)
        return PYTHON_FRIENDLY.get(exc_type, (DEFAULT_MESSAGE, DEFAULT_HINT))
    if language == "java":
        return _translate_java_error(stderr)
    if language == "cpp":
        return _translate_cpp_error(stderr)
    if language == "spring":
        return _translate_spring_error(stderr)
    if language == "node":
        return _translate_node_error(stderr)
    return (DEFAULT_MESSAGE, DEFAULT_HINT)


def _last_exception_type(stderr: str) -> str:
    for line in reversed(stderr.strip().splitlines()):
        line = line.strip()
        if line:
            return line.split(":", 1)[0].strip()
    return ""


def _translate_java_error(stderr: str) -> tuple[str, str]:
    if _JAVA_COMPILE_ERROR_RE.search(stderr):
        return ("Compile error.", "Check the line the compiler points to for a missing semicolon, brace, or type mismatch.")
    match = _JAVA_EXCEPTION_RE.search(stderr)
    exc_type = match.group(1) if match else ""
    return JAVA_FRIENDLY.get(exc_type, (DEFAULT_MESSAGE, DEFAULT_HINT))


def _translate_cpp_error(stderr: str) -> tuple[str, str]:
    if _CPP_COMPILE_ERROR_RE.search(stderr):
        return ("Compile error.", "Check the line the compiler points to for a missing semicolon, brace, or type mismatch.")

    exc_match = _CPP_EXCEPTION_RE.search(stderr)
    if exc_match:
        exc_type = exc_match.group(1)
        message, hint = CPP_FRIENDLY.get(
            exc_type, (f"Uncaught exception ({exc_type}).", "Check the condition that throws this is actually being guarded against."),
        )
        what_match = _CPP_EXCEPTION_WHAT_RE.search(stderr)
        if what_match:
            message = f"{message} ({what_match.group(1).strip()})"
        return (message, hint)

    if "terminate called without an active exception" in stderr:
        return (
            "std::terminate() was called directly.",
            "A common cause: a std::thread that's still joinable (never had join() or detach() called) was destroyed -- join it before it goes out of scope.",
        )

    crash_match = _CPP_CRASH_NOTE_RE.search(stderr)
    if crash_match:
        description = crash_match.group(1)
        if " -- " in description:
            short, hint = description.split(" -- ", 1)
            return (f"{short.strip()}.", f"{hint.strip().capitalize()}.")
        return (f"{description.strip()}.", DEFAULT_HINT)

    return (DEFAULT_MESSAGE, DEFAULT_HINT)


def _translate_spring_error(stderr: str) -> tuple[str, str]:
    if _SPRING_COMPILE_ERROR_RE.search(stderr):
        return ("Compile error.", "Check the line the compiler points to for a missing semicolon, brace, or type mismatch.")

    if _SPRING_ASSERTION_RE.search(stderr):
        detail_match = _SPRING_ASSERTION_DETAIL_RE.search(stderr)
        message = "Test assertion failed."
        if detail_match:
            message = f"Test assertion failed -- expected {detail_match.group(1).strip()}, but was {detail_match.group(2).strip()}."
        return (message, "Check the expected vs. actual value shown below.")

    exc_match = _SPRING_EXCEPTION_RE.search(stderr)
    exc_type = exc_match.group(1) if exc_match else ""
    if exc_type in SPRING_FRIENDLY:
        return SPRING_FRIENDLY[exc_type]
    if exc_type:
        return (f"Test failed ({exc_type}).", "Check the raw output below for details.")
    return ("Test failed.", "Check the raw output below for details.")


def _translate_node_error(stderr: str) -> tuple[str, str]:
    match = _NODE_ERROR_TYPE_RE.search(stderr)
    exc_type = match.group(1) if match else ""
    return NODE_FRIENDLY.get(exc_type, (DEFAULT_MESSAGE, DEFAULT_HINT))


def extract_error_line_number(stderr: str, language: str = "python") -> Optional[int]:
    if language == "spring":
        # JUnit's reflection-based test invocation appends java.base frames
        # (e.g. ArrayList.java:1596) after the actual test file's frame --
        # the first match is the relevant one here, unlike plain Java where
        # the last match (closest to the entry point) is preferred.
        matches = _JAVA_LINE_RE.findall(stderr)
        return int(matches[0]) if matches else None
    if language == "node":
        header_match = _NODE_HEADER_LINE_RE.search(stderr)
        if header_match:
            return int(header_match.group(1))
        frame_match = _NODE_STACK_FRAME_RE.search(stderr)
        return int(frame_match.group(1)) if frame_match else None
    if language == "java":
        pattern = _JAVA_LINE_RE
    elif language == "cpp":
        pattern = _CPP_LINE_RE
    else:
        pattern = _PYTHON_CODE_FRAME_RE
    matches = pattern.findall(stderr)
    return int(matches[-1]) if matches else None
