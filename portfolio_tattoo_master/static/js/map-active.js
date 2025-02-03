
        var map;
        var addressCoordinates = { "lat": 52.497694, "lng": 13.42525 }; // Координаты Manteuffelstraße 77, Berlin
        var targetGoogleMapsUrl = "https://www.google.com/maps/place/Atelier+Jiyu/@52.4973969,13.4248548,19z/data=!4m6!3m5!1s0x47a84f6d887bf145:0xf474b9e198516c82!8m2!3d52.4973961!4d13.4260725!16s%2Fg%2F11p73kq0g0?entry=ttu&g_ep=EgoyMDI1MDEyOS4xIKXMDSoJLDEwMjExMjMzSAFQAw%3D%3D"; // URL для открытия при клике

        var stylez = [{
            featureType: "all",
            elementType: "all",
            stylers: [{ saturation: -25 }]
        }];

       var mapOptions = {
            zoom: 15,
            center: addressCoordinates,
            scrollwheel: true,
            scaleControl: true,
            disableDefaultUI: false,
            zoomControl: true,
            mapTypeControlOptions: {
                mapTypeIds: [google.maps.MapTypeId.ROADMAP, 'gMap']
            }
        };

        // Инициализация карты
        map = new google.maps.Map(document.getElementById("googleMap"), mapOptions);

        // Добавление маркера на Manteuffelstraße 77
        var marker = new google.maps.Marker({
            map: map,
            position: addressCoordinates,
            title: "Manteuffelstraße 77, Berlin"
        });

        // Открытие Google Maps (Atelier Jiyu) при клике на карту
        google.maps.event.addListener(map, 'click', function () {
            window.open(targetGoogleMapsUrl, '_blank'); // Открывает Google Maps в новой вкладке
        });