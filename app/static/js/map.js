var map = L.map('map').setView([-9.648139, -35.717239], 15);
L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 18}).addTo(map);
var removeMarker

// AO CLICAR NO MAPA
map.on('click', markerOnClick).addTo(map);

function markerOnClick(e)
{
    simpleReverseGeocoding(e)
    marker = L.marker([e.latlng.lat, e.latlng.lng])
    adicionarMarcador(marker)
}
  
function adicionarMarcador(marker) {
  // Remove o marcador anterior
  if (removeMarker && map.hasLayer(removeMarker)) {
    map.removeLayer(removeMarker);
  }
  map.addLayer(marker);
  removeMarker = marker
}

async function simpleReverseGeocoding(e) {
    fetch('http://nominatim.openstreetmap.org/reverse?format=json&lat=' + e.latlng.lat + '&lon=' + e.latlng.lng,  
      {
        method: 'POST',      
        credentials: 'same-origin',
        headers:{
          'Content-Type': 'application/json'
        }
      })
    .then(function(response) {
      return response.json();
    }).then(function(json) {
      document.getElementById('endereco').value = json.display_name;
      document.getElementById('latitude').value = json.lat;
      document.getElementById('longitude').value = json.lon;
    }).catch( function(error){      
      console.error(error);
     
  });
  }

  async function simpleGeocoding() {
    const adress = document.getElementById('endereco').value;
 
    const url = 'https://nominatim.openstreetmap.org/search.php?q='+adress+'&dedupe=0&format=jsonv2'
 
    fetch(url,  
      {
        method: 'POST',      
        credentials: 'same-origin',
        headers:{
          'Content-Type': 'application/json'
        }
      })
    .then(function(response) {
      return response.json();
    }).then(function(json) {
      document.getElementById('endereco').value = json[0].display_name;
      const lat = document.getElementById('latitude').value = json[0].lat;
      const lng = document.getElementById('longitude').value = json[0].lon;
      map.setView([lat,lng], 15);
      marker = L.marker([lat, lng])
      adicionarMarcador(marker)
    }).catch( function(error){      
      console.error(error);
    });
 }
