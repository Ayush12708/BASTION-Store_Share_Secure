// Sample files
const files = [
    {name:"Documents", type:"folder"},
    {name:"Photos", type:"folder"},
    {name:"Presentation.pdf", type:"file"},
    {name:"Project.zip", type:"file"},
    {name:"Music.mp3", type:"file"},
    {name:"Design.sketch", type:"file"},
    {name:"Videos", type:"folder"}
];

const fileGrid = document.getElementById("fileGrid");

// Generate file cards
files.forEach(f=>{
    const div = document.createElement("div");
    div.className = "file-card";
    div.innerHTML = f.type==="folder" ? `📁 ${f.name}` : `📄 ${f.name}`;
    fileGrid.appendChild(div);
});


// Upload simulation
document.getElementById("uploadBtn").addEventListener("click",()=>{
    alert("Upload File Dialog (simulate)");
});

// New Folder
document.getElementById("newFolderBtn").addEventListener("click",()=>{
    const folderName = prompt("Enter folder name:");
    if(folderName){
        const div = document.createElement("div");
        div.className = "file-card";
        div.innerHTML = `📁 ${folderName}`;
        fileGrid.appendChild(div);
    }
});


// Sidebar section switching
const sidebarItems = document.querySelectorAll('.sidebar ul li');
const sections = document.querySelectorAll('.section');

sidebarItems.forEach(item => {
    item.addEventListener('click', () => {

        sidebarItems.forEach(i => i.classList.remove('active'));
        item.classList.add('active');

        sections.forEach(s => s.style.display = 'none');

        const sectionId = item.getAttribute('data-section');
        document.getElementById(sectionId).style.display = 'block';
    });
});


// Dropdown toggle
document.querySelectorAll(".dropdown").forEach(drop => {
    drop.addEventListener("click", function(e){
        e.stopPropagation();
        this.querySelector(".dropdown-content").classList.toggle("show");
    });
});

// Close dropdown when clicking outside
document.addEventListener("click", function(){
    document.querySelectorAll(".dropdown-content").forEach(menu=>{
        menu.classList.remove("show");
    });
});


// Logout
document.getElementById("logoutBtn").addEventListener("click", function(){
    localStorage.removeItem("username");
    window.location.href = "login.html";
});
