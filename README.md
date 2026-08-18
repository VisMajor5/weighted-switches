# weighted-switches

Small logic nodes to help with routing, as well as wildcard and random-based workflows in ComfyUI.

## Included nodes

### Weighted Switch

Up to four inputs of any kind. The weights are proportional. Also returns the index of the selected input.

<p align="center">
  <img src="doc/images/weighted_switch.png" alt="Weighted Switch in ComfyUI" width="300">
</p>

Here we have three inputs (in this case, latents of different sizes), each having a 33% chance of being returned.

<p align="center">
  <img src="doc/images/weighted_switch_usage.png" alt="Weighted Switch in ComfyUI" width="300">
</p>

### Weighted Conditional Switch

Up to four inputs of any kind. Uses a selector to apply a defined weight profile. Also returns the index of the selected input.

<p align="center">
  <img src="doc/images/weighted_cond_switch.png" alt="Weighted Conditional Switch in ComfyUI" width="300">
</p>

Here we see that the selector uses an input (INT from 1 to 4), that there are three profiles with actual values, and two inputs. If the provided INT is 1, then the returned input will be a 50/50 between 1 and 2. If the provided INT is 2, then the returned input will be 2. If the provided INT is 3, then the returned input will be 1.

<p align="center">
  <img src="doc/images/weighted_cond_switch_usage.png" alt="Weighted Conditional Switch in ComfyUI" width="300">
</p>


## Installation

From the `custom_nodes` directory in your ComfyUI installation:

```powershell
git clone https://github.com/VisMajor5/weighted-switches.git
```

Restart ComfyUI, then refresh the browser interface. The nodes appear under the Logic/Routing/ category.
