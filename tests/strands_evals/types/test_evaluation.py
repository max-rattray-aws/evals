from strands_evals.types import EvaluationClassification, EvaluationOutput


def test_evaluation_output_defaults_to_graded():
    """An output with no explicit classification defaults to GRADED (backward compatible)."""
    out = EvaluationOutput(score=1.0, test_pass=True)
    assert out.classification == EvaluationClassification.GRADED


def test_evaluation_classification_values():
    """The enum is a str-enum with stable wire values."""
    assert EvaluationClassification.GRADED == "graded"
    assert EvaluationClassification.COULD_NOT_EVALUATE == "could_not_evaluate"
    assert EvaluationClassification.INFORMATIONAL == "informational"


def test_evaluation_output_accepts_explicit_classification():
    out = EvaluationOutput(
        score=0.0,
        test_pass=False,
        classification=EvaluationClassification.COULD_NOT_EVALUATE,
    )
    assert out.classification is EvaluationClassification.COULD_NOT_EVALUATE


def test_evaluation_output_dict_round_trip():
    out = EvaluationOutput(score=0.5, test_pass=True, classification=EvaluationClassification.INFORMATIONAL)
    dumped = out.model_dump()
    assert dumped["classification"] == EvaluationClassification.INFORMATIONAL
    restored = EvaluationOutput.model_validate(dumped)
    assert restored.classification is EvaluationClassification.INFORMATIONAL


def test_evaluation_output_json_round_trip():
    """classification survives JSON serialization (the path EvaluationReport.to_file uses)."""
    out = EvaluationOutput(
        score=0.0,
        test_pass=False,
        classification=EvaluationClassification.COULD_NOT_EVALUATE,
    )
    json_str = out.model_dump_json()
    assert "could_not_evaluate" in json_str
    restored = EvaluationOutput.model_validate_json(json_str)
    assert restored.classification is EvaluationClassification.COULD_NOT_EVALUATE


def test_classification_accepts_raw_string_value():
    """A raw string (e.g. loaded from a JSON dict) validates into the enum."""
    out = EvaluationOutput.model_validate({"score": 1.0, "test_pass": True, "classification": "informational"})
    assert out.classification is EvaluationClassification.INFORMATIONAL
