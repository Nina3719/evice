// Google Map
// let map;

// // Markers for map
// let markers = [];

// // Info window
// let info = new google.maps.InfoWindow();

// Execute when the DOM is fully loaded
$(document).ready(function() {
  //   // Styles for map
  //   // https://developers.google.com/maps/documentation/javascript/styling
  //   let styles = [
  //     // Hide Google's labels
  //     {
  //       featureType: "all",
  //       elementType: "labels",
  //       stylers: [{ visibility: "off" }]
  //     },
  //     // Hide roads
  //     {
  //       featureType: "road",
  //       elementType: "geometry",
  //       stylers: [{ visibility: "off" }]
  //     }
  //   ];
  //   // Options for map
  //   // https://developers.google.com/maps/documentation/javascript/reference#MapOptions
  //   let options = {
  //     center: { lat: 37.4236, lng: -122.1619 }, // Stanford, California
  //     disableDefaultUI: true,
  //     mapTypeId: google.maps.MapTypeId.ROADMAP,
  //     maxZoom: 14,
  //     panControl: true,
  //     styles: styles,
  //     zoom: 13,
  //     zoomControl: true
  //   };
  //   // Get DOM node in which map will be instantiated
  //   let canvas = $("#map-canvas").get(0);
  //   // Instantiate map
  //   map = new google.maps.Map(canvas, options);
  //   // Configure UI once Google Map is idle (i.e., loaded)
  //   google.maps.event.addListenerOnce(map, "idle", configure);
  // Configure application
});

// // Add marker for place to map
// function addMarker(place) {
//   // Add marker to map at place latitude and longitude
//   // https://developers.google.com/maps/documentation/javascript/examples/marker-simple
//   var label = place.place_name;
//   let marker = new google.maps.Marker({
//     position: new google.maps.LatLng(place.latitude, place.longitude),
//     label: label,
//     map: map
//   });
//   console.log(marker.position);

//   // Infowindow with articles popup once marker is clicked.
//   // https://developers.google.com/maps/documentation/javascript/events
//   // https://stackoverflow.com/questions/6611634/google-maps-api-v3-add-event-listener-to-all-markers
//   google.maps.event.addListener(marker, "click", function(event) {
//     // set center to clicked marker
//     map.panTo(marker.position);

//     // Get articles
//     $.getJSON("/articles?geo=" + place.postal_code).done(function(data) {
//       console.log(data);
//       var items = "";

//       // Retrieve first four articles
//       // http://www.echoecho.com/htmllinks01.htm
//       // https://www.w3schools.com/html/html_lists.asp
//       for (i = 0; i < 4; i++) {
//         items +=
//           "<ul>" +
//           "<li>" +
//           "<a href=" +
//           data[i]["link"] +
//           ">" +
//           data[i]["title"] +
//           "</a>" +
//           "</li>" +
//           "</ul>";
//       }
//       // info.setPosition(marker);
//       showInfo(marker, items);
//     });
//   });
//   // Placed marker into markers array
//   markers.push(marker);
// }

// // Remove markers from map
// function removeMarkers() {
//   // Remove marker in markers
//   // https://developers.google.com/maps/documentation/javascript/markers
//   // https://stackoverflow.com/questions/40538786/googlemaps-api-how-to-remove-multiple-markers
//   for (mark in markers) {
//     markers[mark].setMap(null);
//   }
// }

// // Search database for typeahead's suggestions
// function search(query, syncResults, asyncResults) {
//   // Get places matching query (asynchronously)
//   let parameters = {
//     searchq: query
//   };
//   $.getJSON("/search", parameters, function(data, textStatus, jqXHR) {
//     // Call typeahead's callback with search results (i.e., places)
//     asyncResults(data);
//   });
// }

// // Show info window at marker with content
// function showInfo(marker, content) {
//   // Start div
//   let div = "<div id='info'>";
//   if (typeof content == "undefined") {
//     // http://www.ajaxload.info/
//     div += "<img alt='loading' src='/static/ajax-loader.gif'/>";
//   } else {
//     div += content;
//   }

//   // End div
//   div += "</div>";

//   // Set info window's content
//   info.setContent(div);

//   // Open info window (if not already open)
//   info.open(map, marker);
// }

// // Update UI's markers
// function update() {
//   // Get map's bounds
//   let bounds = map.getBounds();
//   let ne = bounds.getNorthEast();
//   let sw = bounds.getSouthWest();

//   // Get places within bounds (asynchronously)
//   let parameters = {
//     ne: `${ne.lat()},${ne.lng()}`,
//     searchq: $("#searchq").val(),
//     sw: `${sw.lat()},${sw.lng()}`
//   };
//   $.getJSON("/update", parameters, function(data, textStatus, jqXHR) {
//     // Remove old markers from map
//     removeMarkers();

//     // Add new markers to map
//     for (let i = 0; i < data.length; i++) {
//       addMarker(data[i]);
//     }
//   });
// }

function configure() {
  console.log("hello111");
  // Update UI after map has been dragged
  // google.maps.event.addListener(map, "dragend", function() {
  //   // If info window isn't open
  //   // http://stackoverflow.com/a/12410385
  //   if (!info.getMap || !info.getMap()) {
  //     update();
  //   }
  // });

  // Update UI after zoom level changes
  // google.maps.event.addListener(map, "zoom_changed", function() {
  //   update();
  // });

  // Configure typeahead
  $("#startq").typeahead(
    {
      highlight: false,
      minLength: 1
    },
    {
      display: function(suggestion) {
        return null;
      },
      limit: 10,
      source: search,
      templates: {
        suggestion: Handlebars.compile(
          "<div>" +
            "{{place_name}}, {{admin_name1}}, {{postal_code}}" +
            "</div>"
        )
      }
    }
  );

  // Re-center map after place is selected from drop-down
  // $("#searchq").on("typeahead:selected", function(
  //   eventObject,
  //   suggestion,
  //   name
  // ) {
  //   // Set map's center
  //   map.setCenter({
  //     lat: parseFloat(suggestion.latitude),
  //     lng: parseFloat(suggestion.longitude)
  //   });

  //   // Update UI
  //   update();
  // });

  // Hide info window when text box has focus
  // $("#searchq").focus(function(eventData) {
  //   info.close();
  // });

  // Re-enable ctrl- and right-clicking (and thus Inspect Element) on Google Map
  // https://chrome.google.com/webstore/detail/allow-right-click/hompjdfbfmmmgflfjdlnkohcplmboaeo?hl=en
  document.addEventListener(
    "contextmenu",
    function(event) {
      event.returnValue = true;
      event.stopPropagation && event.stopPropagation();
      event.cancelBubble && event.cancelBubble();
    },
    true
  );

  // Update UI
  // update();

  // Give focus to text box
  $("#startq").focus();
}

// Search database for typeahead's suggestions
function search(query, syncResults, asyncResults) {
  console.log("hello123");
  // Get places matching query (asynchronously)
  let parameters = {
    startq: query
  };
  $.getJSON("/search", parameters, function(data, textStatus, jqXHR) {
    // Call typeahead's callback with search results (i.e., places)
    asyncResults(data);
  });
}
