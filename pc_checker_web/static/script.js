const screens = [...document.querySelectorAll(".screen")];
function showScreen(id){screens.forEach(s=>s.classList.toggle("active",s.id===id));window.scrollTo({top:0,behavior:"smooth"});}
document.querySelectorAll("[data-screen]").forEach(b=>b.addEventListener("click",()=>showScreen(b.dataset.screen)));
document.querySelectorAll("[data-home]").forEach(b=>b.addEventListener("click",()=>showScreen("home")));
const toast=document.getElementById("toast");
function notify(message){toast.textContent=message;toast.classList.add("show");setTimeout(()=>toast.classList.remove("show"),2200);}
function formData(form){return Object.fromEntries(new FormData(form).entries());}
async function post(url,data){const r=await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});return r.json();}
document.getElementById("specsForm").addEventListener("submit",e=>{e.preventDefault();const d=formData(e.currentTarget);localStorage.setItem("pcCheckerSpecs",JSON.stringify(d));document.getElementById("saveMessage").textContent="Specs saved in this browser. You can use them for checks.";notify("PC specs saved successfully.");});
document.getElementById("bottleneckForm").addEventListener("submit",async e=>{e.preventDefault();const out=document.getElementById("bottleneckResult");out.textContent="Checking...";try{const r=await post("/api/bottleneck",formData(e.currentTarget));out.textContent=r.result;}catch{out.textContent="Could not complete the check. Make sure the Flask app is running.";}});
document.getElementById("compatibilityForm").addEventListener("submit",async e=>{e.preventDefault();const out=document.getElementById("compatibilityResult");out.textContent="Checking...";try{const r=await post("/api/compatibility",formData(e.currentTarget));out.textContent=r.result;}catch{out.textContent="Could not complete the check. Make sure the Flask app is running.";}});
const choices=document.getElementById("troubleshootChoices"),troubleResult=document.getElementById("troubleshootResult"),troubleBack=document.getElementById("troubleBack");
document.querySelectorAll("[data-problem]").forEach(b=>b.addEventListener("click",async()=>{try{const r=await fetch("/api/troubleshoot/"+b.dataset.problem).then(x=>x.json());troubleResult.innerHTML="<h3></h3><ol></ol>";troubleResult.querySelector("h3").textContent=r.problem;const ol=troubleResult.querySelector("ol");r.steps.forEach(step=>{const li=document.createElement("li");li.textContent=step;ol.appendChild(li);});troubleResult.classList.remove("hidden");choices.classList.add("hidden");troubleBack.classList.remove("hidden");}catch{notify("Could not load troubleshooting steps.");}}));
troubleBack.addEventListener("click",()=>{troubleResult.classList.add("hidden");choices.classList.remove("hidden");troubleBack.classList.add("hidden");});
document.getElementById("exitButton").addEventListener("click",()=>notify("You can close this browser tab to exit."));
// Restore saved specs to the input form when available.
const saved=localStorage.getItem("pcCheckerSpecs");
if(saved){try{const d=JSON.parse(saved);const form=document.getElementById("specsForm");Object.entries(d).forEach(([k,v])=>{if(form.elements[k])form.elements[k].value=v;});document.getElementById("saveMessage").textContent="Previously saved specs loaded from this browser.";}catch{}}
