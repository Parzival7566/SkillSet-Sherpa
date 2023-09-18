document.addEventListener("DOMContentLoaded", function () {
  const aptitudeForm = document.getElementById("aptitude-form");

  aptitudeForm.addEventListener("submit", function (event) {
    const formData = new FormData(aptitudeForm);

    // Convert form data to an object
    const answers = {};
    formData.forEach((value, key) => {
      answers[key] = value;
    });

    fetch("http://localhost:5000/aptitude-test", {
      method: "POST",
      headers: {
        "Authorization": "Bearer sk-d2e2a61e82404b62955c08ca93c93c16",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ answers }),
    })
      .then((response) => response.json())
     // Inside the fetch block after a successful submission
.then((data) => {
  if (data.success) {
    alert("Aptitude test submitted successfully!/n You can now close this tab");
    // Close the current tab
    window.close();
  } else {
    alert("Error submitting aptitude test.");
    // Handle the error case
  }
})
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred while submitting the aptitude test.");
      });

    event.preventDefault(); // Prevent the default form submission
  });
});
