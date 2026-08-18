import random
import re

class WeightedConditionalSwitch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "selector": (
                    "INT",
                    {
                        "default": 1,
                        "min": 1,
                        "max": 4,
                        "step": 1,
                    },
                ),

                # Each row is 4 comma-separated weights.
                # Row 1 is used when selector == 1.
                # Row 2 is used when selector == 2.
                # etc.
                #
                # Example:
                # selector == 1:
                # "0, 0.5, 0.5, 0"
                # returns input_2 or input_3 with 50% chance each.
                #
                # selector == 2:
                # "0, 0, 1, 0"
                # returns input_3 with 100% chance.
                "weights_for_selector_1": (
                    "STRING",
                    {
                        "default": "1, 0, 0, 0",
                        "multiline": False,
                        "placeholder": "weight input_1, weight input_2, weight input_3, weight input_4",
                    },
                ),
                "weights_for_selector_2": (
                    "STRING",
                    {
                        "default": "0, 1, 0, 0",
                        "multiline": False,
                        "placeholder": "weight input_1, weight input_2, weight input_3, weight input_4",
                    },
                ),
                "weights_for_selector_3": (
                    "STRING",
                    {
                        "default": "0, 0, 1, 0",
                        "multiline": False,
                        "placeholder": "weight input_1, weight input_2, weight input_3, weight input_4",
                    },
                ),
                "weights_for_selector_4": (
                    "STRING",
                    {
                        "default": "0, 0, 0, 1",
                        "multiline": False,
                        "placeholder": "weight input_1, weight input_2, weight input_3, weight input_4",
                    },
                ),
            },

            "optional": {
                "input_1": "*",
                "input_2": "*",
                "input_3": "*",
                "input_4": "*",
            },
        }

    RETURN_TYPES = ("*", "INT")
    RETURN_NAMES = ("value", "selected_index")
    FUNCTION = "run"
    CATEGORY = "Logic/Routing"

    def parse_weights(self, raw_weights, selector):
        if raw_weights is None:
            raw_weights = ""

        parts = re.split(r"[\s,;]+", raw_weights.strip())
        parts = [p for p in parts if p != ""]

        if len(parts) != 4:
            raise ValueError(
                f"weights_for_selector_{selector} must contain exactly 4 numbers, "
                f"got {len(parts)}: '{raw_weights}'"
            )

        try:
            weights = [float(x) for x in parts]
        except Exception as e:
            raise ValueError(
                f"weights_for_selector_{selector} must contain 4 numeric weights. "
                f"Got: '{raw_weights}'"
            ) from e

        if any(w < 0 for w in weights):
            raise ValueError(
                f"weights_for_selector_{selector} must not contain negative numbers. "
                f"Got: '{raw_weights}'"
            )

        return weights

    def run(
        self,
        selector,
        weights_for_selector_1,
        weights_for_selector_2,
        weights_for_selector_3,
        weights_for_selector_4,
        input_1=None,
        input_2=None,
        input_3=None,
        input_4=None,
    ):
        if selector not in (1, 2, 3, 4):
            raise ValueError("selector must be an INT between 1 and 4.")

        inputs = [input_1, input_2, input_3, input_4]

        weight_strings = [
            weights_for_selector_1,
            weights_for_selector_2,
            weights_for_selector_3,
            weights_for_selector_4,
        ]

        weights = self.parse_weights(weight_strings[selector - 1], selector)

        # Build list of connected/available inputs.
        # In ComfyUI, an unconnected optional input is usually None.
        available_indices = []
        available_weights = []

        for i, value in enumerate(inputs, start=1):
            if value is not None:
                available_indices.append(i)
                available_weights.append(weights[i - 1])

        if len(available_indices) == 0:
            raise ValueError("Connect at least one of input_1, input_2, input_3, input_4.")

        total_weight = sum(available_weights)

        if total_weight <= 0:
            raise ValueError(
                f"selector={selector} has no positive weight for any connected input. "
                "Connect the referenced inputs or increase their weights."
            )

        # Strict behavior:
        # If a positive weight points to an unconnected input, reject the node run.
        # This matches your requirement that the node should not accept an invalid reference.
        for i, value in enumerate(inputs, start=1):
            if value is None and weights[i - 1] > 0:
                raise ValueError(
                    f"selector={selector} has positive weight for unconnected input_{i}. "
                    f"Connect input_{i} or set its weight to 0."
                )

        # Randomly choose one of the available inputs using normalized weights.
        selected_index = random.choices(available_indices, weights=available_weights, k=1)[0]
        selected_value = inputs[selected_index - 1]

        return (selected_value, selected_index)


NODE_CLASS_MAPPINGS = {
    "WeightedConditionalSwitch": WeightedConditionalSwitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WeightedConditionalSwitch": "Weighted Conditional Switch 🎲",
}
