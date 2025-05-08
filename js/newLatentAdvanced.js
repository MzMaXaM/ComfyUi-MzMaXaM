
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
                "Square Format Photography (1:1)": [
                    "1920x1920",
                    "3840x3840",
                    "7680x7680",
                    "1344x1344",
                    "1280x1280",
                    "1216x1216",
                    "1152x1152",
                    "1088x1088",
                    "1024x1024",
                    "960x960",
                    "896x896",
                    "832x832",
                    "768x768",
                    "704x704",
                    "640x640",
                    "576x576",
                    "512x512"
                ],
                "Horizontal Portrait Photography (4:5)": [
                    "1920x1536",
                    "3840x3072",
                    "7680x6144",
                    "1600x1280",
                    "1536x1216",
                    "1280x1024",
                    "960x768"
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