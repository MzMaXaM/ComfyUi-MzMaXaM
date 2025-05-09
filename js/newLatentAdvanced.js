
import { app } from "../../scripts/app.js"; // Adjust the relative path as needed
app.registerExtension({
    name: "newLatentAdvanced_dynamicUI_nodeCreated", // Changed extension name slightly
    async nodeCreated(node) {
        // Check if the created node is our specific node type
        if (node.comfyClass === "newLatentAdvanced") {
            // Find the aspect_ratio and resolution widgets by their names
            const aspectSelect = node.widgets.find(w => w.name === "aspect_ratio");
            const resolutionSelect = node.widgets.find(w => w.name === "resolution");
            // If widgets are not found (shouldn't happen if INPUT_TYPES is correct, but good check)
            if (!aspectSelect || !resolutionSelect) {
                console.error("[NewLatentAdvanced] ERROR: Could not find aspect_ratio or resolution widgets on the node.");
                return;
            }
            // Our resolution mapping must mirror the backend mapping exactly.
            const resolutionMapping = {
                "1:1 Square Format": [
                    "Divisible by 64 512x512",
                    "Divisible by 64 576x576",
                    "Divisible by 64 640x640",
                    "Divisible by 64 704x704",
                    "Divisible by 64 768x768",
                    "Divisible by 64 832x832",
                    "Divisible by 64 896x896",
                    "Divisible by 64 960x960",
                    "Divisible by 64 1024x1024",
                    "Divisible by 64 1088x1088",
                    "Divisible by 64 1152x1152",
                    "Divisible by 64 1216x1216",
                    "Divisible by 64 1280x1280",
                    "Divisible by 64 1344x1344",
                    "Divisible by 64 1920x1920"
                ],
                "3:4 Portrait Photography, Retro CRT TV & Monitor": [
                    "Divisible by 64 576x768",
                    "Divisible by 64 768x576",
                    "Divisible by 64 768x1024",
                    "Divisible by 64 960x1280",
                    "Divisible by 64 1024x768",
                    "Divisible by 8 1088x1472",
                    "Divisible by 8 1472x1088",
                    "Divisible by 64 1152x1536",
                    "Divisible by 64 1280x960",
                    "Divisible by 64 1440x1920",
                    "Divisible by 64 1536x1152",
                    "Divisible by 64 1920x1440"
                ],
                "4:5 Instagram Portrait": [
                    "Divisible by 64 768x960",
                    "Divisible by 64 960x768",
                    "Divisible by 64 1024x1280",
                    "Divisible by 64 1216x1536",
                    "Divisible by 64 1280x1024",
                    "Divisible by 64 1280x1600",
                    "Divisible by 64 1536x1216",
                    "Divisible by 64 1536x1920",
                    "Divisible by 64 1600x1280",
                    "Divisible by 64 1920x1536"
                ],
                "2:3 Standard Photography": [
                    "Divisible by 64 512x768",
                    "Divisible by 64 768x512",
                    "Divisible by 64 768x1152",
                    "Divisible by 64 896x1344",
                    "Divisible by 64 1024x1536",
                    "Divisible by 64 1152x768",
                    "Divisible by 64 1152x1728",
                    "Divisible by 64 1280x1920",
                    "Divisible by 64 1344x896",
                    "Divisible by 64 1536x1024",
                    "Divisible by 64 1728x1152",
                    "Divisible by 64 1920x1280",
        ]
            };
            // This function updates the options in the resolution dropdown widget
            function updateResolutionOptions() {
              const selectedAspect = aspectSelect.value; // Get value directly from the widget
              const optionsArray = resolutionMapping[selectedAspect] || [];
              console.log("[NewLatentAdvanced] Options for selected aspect:", optionsArray);
              // Update the widget's options directly
              // The 'options' property on a combo/dropdown widget holds its available values.
              resolutionSelect.options.values = optionsArray;
              // Set the value of the resolution widget to the first option in the new list
              // This also updates the displayed value in the UI.
              if (optionsArray.length > 0) {
                  resolutionSelect.value = optionsArray[0];
                   // *** Added: Explicitly dispatch a change event on the underlying element ***
                   // This can help ensure ComfyUI's frontend/backend state is synchronized
                   if (resolutionSelect.element) { // Check if the underlying element exists
                        resolutionSelect.element.dispatchEvent(new Event('change'));
                   }
              } else {
                  resolutionSelect.value = ""; // Set to empty if no options
                    if (resolutionSelect.element) {
                        resolutionSelect.element.dispatchEvent(new Event('change'));
                    }
              }
               app.canvas.draw(true); // Force redraw
          }
            aspectSelect.callback = updateResolutionOptions;
            // Perform an initial update when the node is created
            updateResolutionOptions();
        }
    }
});