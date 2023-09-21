# jQuery ile Girdi Tamamlamak (Auto Complete)

Form uzerinde metin bazli alanlarda girilecek birkac harf sonrasi
seceneklerin bize bir listede gosterilmesini istiyorsak (suggest,
autocomplete), suradaki jQuery plug-in ise yarayacaktir. Indirip
jquery.autocomplete.js ve jquery.autocomplete.css dosyalarini dizin
yapiniza ekleyin ve HTML dosyalari icinden "link href" ve "script src"
ile dahil edin. Kod kullanimi oldukca basit, form uzerindeki tipi text
olan input alaninin kimligini (id) alip, autocomplete koduna
geciyoruz. Eger id "kimlik1" olsaydi, jQuery ile

```html
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Autocomplete - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.13.2/themes/base/jquery-ui.css">
  <script src="https://code.jquery.com/jquery-3.6.0.js"></script>
  <script src="https://code.jquery.com/ui/1.13.2/jquery-ui.js"></script>
  <script>
  $( function() {
    var availableTags = [
      "ActionScript",
      "AppleScript",
      "Asp",
      "BASIC"
    ];
    $( "#tags" ).autocomplete({
      source: availableTags
    });
  } );
  </script>
</head>
<body>
 
<div class="ui-widget">
  <label for="tags">Tags: </label>
  <input id="tags">
</div>
  
</body>
</html>
```

kullanabilirdik. Degisken "liste" bir Javascript dizinidir; JSON ile
servis tarafindan alinmis olabilir, ya da yerel olarak gomulu
(hardcoded) bir liste olabilir, vs.

