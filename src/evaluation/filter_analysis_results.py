import os
import pandas as pd
import numpy as np
import re


def filter_python_pylint(pylint_report_txt_path):
    """Filter Python code for specific issues detected by pylint."""
    report_path = pylint_report_txt_path
    return_lines = []

    remove_list = [
        "C0301", "C0305", "C0303", "C0304", "C0103", "C0112", "C0114", "C0115", "C0116",
        "C0410", "C0411", "C0412", "C0413", "C0414", "C0415", "R0903", "W0611", "W0401",
        "E0602", "W0621"
    ]

    with open(report_path, "r") as f:
        lines = f.readlines()

    if not lines:
        return []

    for line in lines:
        if line.startswith(file_name) and line.split(": ")[1] not in remove_list:
            return_lines.append(line)

    return return_lines


def filter_python_flake8(flake8_report_txt_path):
    """Filter Python code for specific issues detected by flake8."""
    report_path = flake8_report_txt_path
    return_lines = []

    remove_list = [
        "F821", "W292", "E265", "E231", "W293", "E261", "E501", "E262", "W291", "E225",
        "E227", "E302", "E303", "E305", "E211", "E228", "E275", "E402", "E201", "E203"
    ]

    with open(report_path, "r") as f:
        lines = f.readlines()

    if not lines:
        return []

    for line in lines:
        line = line.replace(f"path/to/data/results/reports/python/flake8/", "")
        if line.split(" ")[1] not in remove_list:
            return_lines.append(line)

    return return_lines


def filter_java_pmd(pmd_report_txt_path):
    """Filter Java code for specific issues detected by PMD."""
    report_path = pmd_report_txt_path
    return_lines = []

    remove_list = [
        "CommentRequired", "NoPackage", "AtLeastOneConstructor", "LocalVariableCouldBeFinal",
        "UseVarargs", "MethodArgumentCouldBeFinal", "ShortVariable", "OnlyOneReturn", "LawOfDemeter",
        "ControlStatementBraces", "CommentDefaultAccessModifier", "CommentSize", "AvoidLiteralsInIfCondition",
        "ImmutableField", "CognitiveComplexity", "CyclomaticComplexity", "FormalParameterNamingConventions",
        "UseUnderscoresInNumericLiterals", "AvoidReassigningLoopVariables", "ShortClassName", "AvoidInstantiatingObjectsInLoops",
        "OneDeclarationPerLine", "SystemPrintln", "LongVariable", "LocalVariableNamingConventions"
    ]

    if not os.path.exists(report_path):
        return []

    with open(report_path, "r") as f:
        lines = f.readlines()

    if not lines:
        return []

    for line in lines:
        line = line.replace(f"path/to/data/results/reports/java/pmd/", "")

        if "ParseException" in line:
            return_lines.append(line)
            return return_lines

        if line.split("\t")[1].replace(":", "") not in remove_list:
            return_lines.append(line)

    return return_lines


def filter_java_checkstyle(checkstyle_report_txt_path):
    """Filter Java code for specific issues detected by Checkstyle."""
    report_path = checkstyle_report_txt_path
    return_lines = []

    remove_list = ["JavadocPackage", "NewlineAtEndOfFile", "WhitespaceAround", "WhitespaceAfter", "LineLength",    "RegexpSingleline", "JavadocVariable", "FinalParameters", "MagicNumber", "NeedBraces",    "NoWhitespaceBefore", "LocalVariableName", "OperatorWrap", "AvoidStarImport", "InvalidJavadocPosition",    "NoWhitespaceAfter", "ParenPad", "MethodParamPad", "ParameterName", "LocalFinalVariableName",    "ConstantName", "MethodName", "StaticVariableName", "MemberName", "JavadocMethod", "MissingJavadocMethod",    "JavadocStyle", "DesignForExtension"]

    if not os.path.exists(report_path):
        return []

    with open(report_path, "r") as f:
        lines = f.readlines()

    if not lines:
        return []

    for line in lines:
        if line.startswith("[ERROR]"):
            line = line.replace("[ERROR] ", "")
            line = line.replace(f"path/to/data/results/reports/java/checkstyle/", "")
            type_smell = line.split(". [")[1].replace("]", "").strip()

            if type_smell not in remove_list:
                return_lines.append(line)

    return return_lines


if __name__ == "__main__":
    path_report_pylint = "path/to/data/results/reports/python/pylint/001-two-sum.txt"
    filter_python_pylint(path_report_pylint)
