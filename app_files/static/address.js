
var searchnames= [];
  /////////////////////////////////////////////////UPDATE

// console.log(searchnames);

var account_num=[];
// console.log(account_num);

d3.json('/addresses',).then(data => {
    // console.log(data);
    var addresses = data.map(data => data.address);
    // console.log(addresses);
    const uniqueSet= new Set(addresses);
    const backToArray= [...uniqueSet];
    console.log(backToArray.length);
    //Push names to searchnames global variable, to be read in to search.js
    
    for (var i=0; i<backToArray.length;i++){
      searchnames.push(backToArray[i]);
    };

//Select the Select button in order to pull the input address
var button = d3.select("#button");
button.on("click", function grab() {
var inputaddress=[];

//Clear Table of default or filtered data
var input = document.getElementById("myInput").value;
inputaddress.push(input);
// console.log(inputaddress[0]);

//Function to filter data by the Input Value
function address(x){return (x.address ===inputaddress[0]);}

//Store filtered data in chosen variable 
var chosen = data.filter(address);
// console.log(chosen);
// console.log(chosen[0].account_number);
var account_chosen= (Object.values(chosen[0].account_number));
// console.log(account_chosen);
account_num.splice(0,1,chosen[0].account_number);
// console.log(chosen[0].account_number);    
// console.log(account_num);
//Test filter with the chosen account_number by filtering data by the account number to return the address

d3.json(`/prediction/${account_num}`).then(predictions_data => {
  console.log(predictions_data);
  var approved= String(predictions_data.prediction)
  //var probability= Math.round(predictions_data.confidence*100)
  var tot_val= String(predictions_data.tot_val)
  var tot_val_pred= String(predictions_data.tot_val_pred)
  // console.log(approved);
  console.log(tot_val_pred);
  document.getElementById("tot_val_tag").innerHTML = `Your current appraised value is ${tot_val} and your predicted value is ${tot_val_pred} `;

if(approved== "Yes"){
  document.getElementById('approval_img').src ="https://raw.githubusercontent.com/mharvanek/00_Group_Project_04/stu/approved.JPG";
  document.getElementById("approval_tag").innerHTML = "We recommend contacting the Dallas Appraisal District to appeal your current tax rate!";
  } else{  
  document.getElementById('approval_img').src ="https://raw.githubusercontent.com/mharvanek/00_Group_Project_04/stu/not_approved.JPG";
  document.getElementById("approval_tag").innerHTML = "At this time, appealing your current tax rate is not likely to be succesful.";
  }
    });
      
d3.json(`/attributes/${account_num}`).then(features => {
  // console.log(features);
  
  // console.log(features[0].total_living_square_feet/100);
});

});

});

//Autocomplte Function
  $("#myInput").autocomplete({ 
    maxResults: 5,
    autoFocus: true,
    source: function(request, response) {
        var results = $.ui.autocomplete.filter(searchnames, request.term);
        
        response(results.slice(0, this.options.maxResults));
    }
});


