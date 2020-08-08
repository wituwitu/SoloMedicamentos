$(document).ready(function() {
    
    $('#searchButton').click(function() {
        med_name = document.getElementById("med_name").value;
        console.log("Buscando medicamento: " + med_name);
        $.getJSON($SCRIPT_ROOT + '/_searchMed', {
            medName: med_name            
        }, function(data) {
            console.log(data);
            var table = document.getElementById("results");
            var errorDiv = document.getElementById("Error");
            table.innerHTML = "";
            errorDiv.innerHTML = "";
            if(Object.keys(data.result).length === 0)
            {
                errorDiv.innerHTML = "<p>No se ha encontrado el medicamento.</p>";
            }
            else {
                var header = table.insertRow(0);
                header.innerHTML= "<th>Farmacia</th><th>Precio</th><th>Dirección</th>";
                
                var i = 0;
                for (var key in data.result) {
                    i += 1;
                    var row = table.insertRow();
                    row.innerHTML= "<td>" + key + "</td><td>" + data.result[key]["price"] + " $</td><td><a href=" + data.result[key]["url"] + ">" + data.result[key]["url"] + "</a></td>";
                }
            }
            
        });

    });
})