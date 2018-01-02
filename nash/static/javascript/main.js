if (location.hash == '#good') {
    document.getElementById('result').innerHTML = '<div class="good-result">File uploaded successfully.</div>';
    setTimeout(function() {
      document.getElementById('result').remove();
    }, 2000);
  } else if (location.hash == '#error') {
    document.getElementById('result').innerHTML = '<div class="error-result">Error while loading the file.</div>';
  }