 let cardShow= document.querySelector("#cardShow");
 let discriptionCardShow=document.querySelector("#discriptionCardShow");
 let card=document.querySelectorAll(".card");
 let descriptionCard=document.querySelectorAll(".description-card");
let imgCard=document.querySelectorAll(".img-card");
  
 cards();

 function cards(){
    for(let i=0;i<card.length;i++){
    descriptionCard[i].style.display= "none" ;
    imgCard[i].style.width="100%";
    card[i].style.border="none";
    }
 }
 cardShow.addEventListener("click",cards);

 discriptionCardShow.addEventListener("click",function(){
    for(let i=0;i<card.length;i++){
         card[i].style.display="flex"                 
         imgCard[i].style.width="50%";
         descriptionCard[i].style.display="flex";
         
    }
 })

  