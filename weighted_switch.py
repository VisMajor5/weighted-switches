import random


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


ANY = AnyType("*")


class WeightedSwitch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 0xffffffffffffffff,
                    },
                ),
            },
            "optional": {
                "input_1": (ANY, {}),
                "weight_1": ("INT", {"default": 50, "min": 0, "max": 100}),
                "input_2": (ANY, {}),
                "weight_2": ("INT", {"default": 50, "min": 0, "max": 100}),
                "input_3": (ANY, {}),
                "weight_3": ("INT", {"default": 0, "min": 0, "max": 100}),
                "input_4": (ANY, {}),
                "weight_4": ("INT", {"default": 0, "min": 0, "max": 100}),
            },
        }

    RETURN_TYPES = (ANY, "INT")
    RETURN_NAMES = ("value", "selected_input")
    FUNCTION = "get_random_choice"
    CATEGORY = "Logic/Routing"

    def get_random_choice(
        self,
        seed,
        input_1=None,
        weight_1=0,
        input_2=None,
        weight_2=0,
        input_3=None,
        weight_3=0,
        input_4=None,
        weight_4=0,
    ):
        rng = random.Random(seed)

        candidates = []

        if input_1 is not None and weight_1 > 0:
            candidates.append((1, input_1, weight_1))

        if input_2 is not None and weight_2 > 0:
            candidates.append((2, input_2, weight_2))

        if input_3 is not None and weight_3 > 0:
            candidates.append((3, input_3, weight_3))

        if input_4 is not None and weight_4 > 0:
            candidates.append((4, input_4, weight_4))

        if not candidates:
            raise ValueError(
                "Weighted Random Any requires at least one connected input with a non-zero weight."
            )

        weights = [candidate[2] for candidate in candidates]

        selected_position = rng.choices(
            range(len(candidates)),
            weights=weights,
            k=1,
        )[0]

        selected_input_number, selected_value, _ = candidates[selected_position]

        return (selected_value, selected_input_number)


NODE_CLASS_MAPPINGS = {
    "WeightedSwitch": WeightedSwitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WeightedSwitch": "Weighted Switch 🎲",
}
