/* Getting side navbar with hamburger/toggle button when screen is small*/

const hamburger = document.querySelector(".hamburger");
const sidenav= document.querySelector(".sidenav");
const links= document.querySelectorAll(".sidenav div");

hamburger.addEventListener("click", () => {
	sidenav.classList.toggle("open");
  // document.body.style.overflow = "hidden";
} );


/* Dropdown in side navbar */
var dropdown = document.getElementsByClassName("dropdown-btn");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
  document.getElementById("a").innerHTML = "-";
  this.classList.toggle("active");
  var dropdownContent = this.nextElementSibling;
  if (dropdownContent.style.display === "block") {
  dropdownContent.style.display = "none";
  document.getElementById("a").innerHTML = "+";
  } else {
  dropdownContent.style.display = "block";
  }
  });
}



/* Dropdown in horizontal navbar */

function dropFunction() {
  document.getElementById("user-dropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.user_name')) {
    var dropdowns = document.getElementsByClassName("drop-cont");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}