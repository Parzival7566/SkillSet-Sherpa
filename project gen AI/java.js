function askForMarksheet() {
    appendMessage(PERSON_NAME, PERSON_IMG, "right", "Yes");
    appendMessage(BOT_NAME, BOT_IMG, "left", "Great! Please upload your marksheet.");
  
    // Add an upload button
    const uploadButtonHTML = `
      <input type="file" id="uploadMarksheet" accept="image/*">
      <button onclick="uploadMarksheet()">Upload</button>
    `;
    appendMessage(BOT_NAME, BOT_IMG, "left", uploadButtonHTML);
  }
  
  // Function to ask for image upload
  function askForImage() {
    appendMessage(PERSON_NAME, PERSON_IMG, "right", "No");
    appendMessage(BOT_NAME, BOT_IMG, "left", "Okay! If you change your mind, you can upload it later.");
  }
  
  // Function to handle marksheet upload
  function uploadMarksheet() {
    const uploadInput = document.getElementById('uploadMarksheet');
    const file = uploadInput.files[0];
  
    if (file) {
      // You can handle the uploaded file here (e.g., send it to a server, process it)
      // For simplicity, we'll just display a message
      appendMessage(PERSON_NAME, PERSON_IMG, "right", "Marksheet uploaded successfully!");
    } else {
      appendMessage(PERSON_NAME, PERSON_IMG, "right", "No file selected. Please choose a marksheet to upload.");
    }
    // ... (Previous code)
  
  function uploadMarksheet() {
    const uploadInput = document.getElementById('uploadMarksheet');
    const file = uploadInput.files[0];
  
    if (file) {
      // Store the uploaded image in the variable
      uploadedImage = URL.createObjectURL(file);
  
      // Display the selected image
      const uploadedImageContainer = get("#uploadedImageContainer");
      uploadedImageContainer.innerHTML = `<img src="${uploadedImage}" alt="Uploaded Image" class="uploaded-image">`;
  
      // You can handle the uploaded file here (e.g., send it to a server, process it)
      // For simplicity, we'll just display a message
      appendMessage(PERSON_NAME, PERSON_IMG, "right", "Marksheet uploaded successfully!");
    } else {
      appendMessage(PERSON_NAME, PERSON_IMG, "right", "No file selected. Please choose a marksheet to upload.");
    }
  }
  
  // Function to open the uploaded image
  function openUploadedImage() {
    if (uploadedImage) {
      window.open(uploadedImage, "_blank");
    } else {
      alert("No image has been uploaded yet.");
    }
  }
  
  // ... (Remaining code)
  
  // Updated JavaScript code for the aptitude test
  let aptitudeQuestions = [
    {
      question: "Question 1: What is 2 + 2?",
      options: ["A. 3", "B. 4", "C. 5", "D. 6"],
      answer: "B"
    },
    {
      question: "Question 2: Which planet is closest to the sun?",
      options: ["A. Earth", "B. Mars", "C. Venus", "D. Jupiter"],
      answer: "C"
    },
    // Add more questions here
  ];
  
  let currentQuestionIndex = 0;
  let userAnswers = [];
  
  function StartAptitudeTest()
  {
    appendMessage(BOT_NAME, BOT_IMG, "left", "Great! Let's begin the aptitude test.");
    showNextQuestion();
  }
  
  function showNextQuestion() {
    if (currentQuestionIndex < aptitudeQuestions.length) {
      const question = aptitudeQuestions[currentQuestionIndex];
      const questionHTML = `
        <div class="aptitude-question">
          <label>${question.question}</label>
          <div class="aptitude-options">
            ${question.options.map(option => `<label><input type="radio" name="q${currentQuestionIndex}" value="${option}"> ${option}</label>`).join('')}
          </div>
        </div>
      `;
      const aptitudeTestContainer = get("#aptitude-test-container");
      aptitudeTestContainer.innerHTML = questionHTML;
  
      currentQuestionIndex++;
    } else {
      finishAptitudeTest();
    }
  }
  
  function finishAptitudeTest() {
    appendMessage(BOT_NAME, BOT_IMG, "left", "Thank you for taking the aptitude test!");
  
    // Calculate the score here if needed
  
    currentQuestionIndex = 0;
    userAnswers = [];
    hideAptitudeTest();
  }
  
  function hideAptitudeTest() {
    const aptitudeTestContainer = get("#aptitude-test-container");
    aptitudeTestContainer.innerHTML = "";
  }
  
  function submitAptitudeTest() {
    const answers = [];
    for (let i = 0; i < aptitudeQuestions.length; i++) {
      const selectedOption = get(`input[name="q${i}"]:checked`);
      if (selectedOption) {
        answers.push(selectedOption.value);
      }
    }
  
    // Store or process user answers as needed
    userAnswers = answers;
  
    // You can calculate the score or provide feedback here if needed
  
    appendMessage(BOT_NAME, BOT_IMG, "left", "Aptitude test submitted!");
  
    // Hide the aptitude test
    hideAptitudeTest();
  }
  
  // Add this function to the existing JavaScript code
  function showAptitudeTest() {
    const aptitudeTestContainer = get("#aptitude-test-container");
    aptitudeTestContainer.style.display = "block";
    showNextQuestion();
  }
  
  // Add this line to the botResponse function to show the aptitude test
  if (rawText.toLowerCase().includes("aptitude test")) {
    showAptitudeTest();
  }
  }
  