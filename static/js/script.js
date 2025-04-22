const box = document.querySelector(".input-box");
fileInput = box.querySelector(".input-field");

box.addEventListener("click", () => {
  fileInput.click();
});

fileInput.addEventListener("change", function (event) {
  const file = event.target.files[0];
  console.log(file);
  console.log(file.name);

  if (file) {
    const uploadingSection = document.getElementById("progressArea");
    const uploadingFileName = document.getElementById("uploadingFileName");
    const uploadProgress = document.getElementById("uploadingProgress");
    const uploadPercentage = document.getElementById("uploadingPercentage");


    const uploadedSection = document.getElementById("uploadedArea");
    const uploadedFileName = document.getElementById("uploadedFileName");
    const uploadedFileSize = document.getElementById("uploadedFileSize");


    //Format file name if longer than 10 characters
    let fileName = file.name;
    if (fileName.length > 10) {
      const fileExtension = fileName.substring(fileName.lastIndexOf('.'));
      const start = fileName.substring(0, 5);
      const end = fileName.substring(fileName.length - 5 - fileExtension.length);
      fileName = `${start}...${end}`;
    }
    console.log(fileName);

    uploadingFileName.textContent = `${fileName} - Uploading`;
    uploadingSection.style.display = "block";
    uploadedSection.style.display = "none";

    //Create a FormData object
    const formData = new FormData();
    formData.append("file", file);
    console.log(formData);

    //Create an XMLHttpRequest
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/upload", true);

    //Track progress
    xhr.upload.onprogress = function (event) {
      if (event.lengthComputable) {
        const percentage = Math.round((event.loaded / event.total) * 100);
        uploadProgress.style.width = `${percentage}%`;
        uploadPercentage.textContent = `${percentage}%`;
      }
    };

    //On upload complete
    xhr.onload = function () {
      if (xhr.status === 200) {
        const response = JSON.parse(xhr.responseText);
        uploadingSection.style.display = "none";
        uploadedSection.style.display = "block";
        uploadedFileName.textContent = `${fileName} - Uploaded`;
        uploadedFileSize.textContent = response.file_size;
        console.log(response.message)
      } else {
        alert("File upload failed.");
        console.log(xhr.status)
      }
    };

    //Handle error
    xhr.onerror = function () {
      alert("Error during file upload.");
    };

    //Send the file
    xhr.send(formData);
  }
});

