
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
                    "512x512",
                    "576x576",
                    "640x640",
                    "704x704",
                    "768x768",
                    "832x832",
                    "896x896",
                    "960x960",
                    "1024x1024",
                    "1088x1088",
                    "1152x1152",
                    "1216x1216",
                    "1280x1280",
                    "1344x1344",
                    "1920x1920"
                ],
                "4:5 Portrait Photography": [
                    "512x640",
                    "576x720",
                    "768x960",
                    "1024x1280",
                    "1216x1536",
                    "1280x1600",
                    "1536x1920"
                ],
                "3:4 Retro CRT TV & Monitor": [
                    "576x768",
                    "640x768",
                    "704x896",
                    "768x1024",
                    "960x1280",
                    "1088x1472",
                    "1152x1536",
                    "1440x1920"
                ],
                "2:3 Standard Photography": [
                    "512x768",
                    "576x864",
                    "640x960",
                    "704x1088",
                    "768x1152",
                    "832x1280",
                    "896x1344",
                    "960x1536",
                    "1024x1536",
                    "1152x1728",
                    "1280x1920"
                ],
                "7:10 Trading Cards of all sorts": [
                    "512x728",
                    "576x816",
                    "640x912",
                    "704x1008",
                    "768x1088",
                    "960x1344",
                    "1352x1920"
                ],
                "5:8 Expanded Portrait": [
                    "512x640",
                    "576x720",
                    "640x800",
                    "704x1152",
                    "768x1280",
                    "832x1408",
                    "960x1664",
                    "1024x1792",
                    "1088x1920"
                ],
                "7:12 Tall Vista":[
                     "512x896",
                    "576x1008",
                    "640x1120",
                    "704x1232",
                    "768x1344",
                    "832x1456",
                    "896x1536",
                    "960x1680"
                ],
                "9:16 Smartphone Screen": [
                    "576x1024",
                    "640x1152",
                    "720x1280",
                    "768x1408",
                    "832x1472",
                    "960x1728",
                    "1080x1920"
                ],
                "1:1.85 Cinematic Widescreen": [
                    "512x960",
                    "540x1024",
                    "576x1088",
                    "640x1216",
                    "704x1344",
                    "768x1472",
                    "832x1536",
                    "960x1792",
                    "1024x1920"
                ],
                "1:2 Two Fold": [
                    "512x1024",
                    "576x1152",
                    "640x1280",
                    "704x1408",
                    "768x1536",
                    "832x1664",
                    "896x1792",
                    "960x1920",
                    "1024x2048"
                ],
                "9:21 UltraWide Monitor": [
                    "512x1152",
                    "576x1280",
                    "768x1856",
                    "800x1920",
                    "896x2176"
                ],
                "1:3 Panoramic Photography": [
                    "512x1536",
                    "576x1728",
                    "640x1920"
                ],
                "9:32 Super UltraWide Monitor": [
                    "512x1856",
                    "540x1920",
                    "576x2048",
                    "640x2240",
                    "704x2496"
                ],
                "1:4 Panoramic Photography": [
                    "480x1920",
                    "512x2048",
                    "576x2304",
                    "640x2560",
                    "704x2816"
                ],
                "1:5 Super Panoramic Photography": [
                    "512x2560",
                    "576x2816",
                    "640x3072",
                    "704x3328",
                    "768x3584",
                    "832x3840"
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