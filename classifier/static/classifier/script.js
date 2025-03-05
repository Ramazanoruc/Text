// Sayfa yüklendiğinde çalışacak fonksiyon
document.addEventListener('DOMContentLoaded', function() {
    console.log('Sayfa yüklendi.');

    // Form elemanlarını alıyoruz
    const form = document.querySelector('form');
    const descriptionInput = document.querySelector('#description');
    const submitButton = document.querySelector('button');
    
    // Formun gönderilmesini engellemek için
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // Kullanıcıdan gelen açıklamayı alalım
        const description = descriptionInput.value.trim();

        // Eğer açıklama boşsa uyarı ver
        if (!description) {
            alert('Lütfen bir açıklama girin!');
        } else {
            // Açıklama varsa, formu gönderme
            alert('Form gönderiliyor...');

            // Burada AJAX kullanarak formu gönderebilirsiniz (opsiyonel)
            // Örneğin, fetch API veya jQuery ile veri gönderme
            // fetch(...) veya $.ajax(...) kodları eklenebilir.
        }
    });

    // Kullanıcı, metni değiştirdiğinde formu tekrar kontrol et
    descriptionInput.addEventListener('input', function() {
        if (descriptionInput.value.trim() !== '') {
            submitButton.disabled = false;  // Butonu aktif et
        } else {
            submitButton.disabled = true;   // Butonu devre dışı bırak
        }
    });
});
