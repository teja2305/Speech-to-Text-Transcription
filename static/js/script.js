window.onload = function () {
   // Hide all input options initially
   const inputDivs = document.getElementsByClassName("input_div");
   for (let div of inputDivs) {
     div.style.display = "none";
   }
   document.getElementById("transcript-container").style.display = "none";
 };
 
 document.getElementById("input_type").addEventListener("change", function () {
   const selectedInput = this.value;
   const inputDivs = document.getElementsByClassName("input_div");
 
   for (let div of inputDivs) {
     div.style.display = "none";
   }
 
   switch (selectedInput) {
     case "microphone":
       document.getElementById("microphone_input").style.display = "block";
       break;
     case "audio_file":
       document.getElementById("audio_file_input").style.display = "block";
       break;
     case "video_file":
       document.getElementById("video_file_input").style.display = "block";
       break;
   }
 });
 
 $("form").on("submit", function () {
   $("#loading-screen").show();
 });
 
 $(document).ajaxComplete(function () {
   $("#loading-screen").hide();
 });
 $(document).ajaxComplete(function () {
   // Hide the loading screen
   $("#loading-screen").hide();
 
   // Show the transcript
   document.getElementById("transcript-container").style.display = "block";
 });
 