function uploadImage() {
    const fileInput = document.getElementById("imageInput");
    const file = fileInput.files[0];
    if (!file) {
        alert("Please select an image first!");
        return;
    }

    const formData = new FormData();
    formData.append("image", file);

    fetch("/", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("result").innerText = data.error;
        } else {
            document.getElementById("result").innerHTML = 
                `<h2>Roundness: ${data.roundness.toFixed(2)}%</h2>
                 <p>${data.comment}</p>`;
            document.getElementById("imageDisplay").innerHTML = 
                `<img src="${data.image_url}" alt="Uploaded Chappathi">`;
        }
    })
    .catch(err => {
        console.error("Error:", err);
    });
}
