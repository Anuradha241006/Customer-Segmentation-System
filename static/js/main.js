// =============================================
// InsightAI - Main JavaScript
// =============================================

// Fade out flash messages automatically
document.addEventListener("DOMContentLoaded", function () {

    const flashMessages =
        document.querySelectorAll(".flash-message");

    flashMessages.forEach(function (message) {

        setTimeout(function () {

            message.style.opacity = "0";
            message.style.transform = "translateY(-10px)";
            message.style.transition = "0.4s";

            setTimeout(function () {
                message.remove();
            }, 400);

        }, 4000);

    });

});
// Show selected file name
const datasetInput = document.getElementById("dataset");
const fileName = document.getElementById("file-name");

if (datasetInput && fileName) {

    datasetInput.addEventListener("change", function () {

        if (this.files.length > 0) {
            fileName.textContent = this.files[0].name;
        }

    });

}