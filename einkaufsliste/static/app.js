document.addEventListener('DOMContentLoaded', function() {

    // Edit-Button
    document.querySelectorAll('.editBtn').forEach(btn => {
        btn.addEventListener('click', function() {
            const row = btn.closest('tr');
            row.querySelectorAll('.text').forEach(el => el.style.display = 'none');
            row.querySelectorAll('.edit').forEach(el => el.style.display = 'inline');
            btn.style.display = 'none';
            row.querySelector('.saveBtn').style.display = 'inline';
        });
    });

    // Save-Button
    document.querySelectorAll('.saveBtn').forEach(btn => {
        btn.addEventListener('click', function() {
            const row = btn.closest('tr');
            const id = row.dataset.id;
            const menge = row.querySelectorAll('input')[0].value;
            const einheit = row.querySelectorAll('input')[1].value;
            const artikel = row.querySelectorAll('input')[2].value;

            fetch('./update/' + id, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ menge, einheit, artikel })
            }).then(response => {
                if(response.ok){
                    row.querySelectorAll('.text')[0].textContent = menge;
                    row.querySelectorAll('.text')[1].textContent = einheit;
                    row.querySelectorAll('.text')[2].textContent = artikel;
                    row.querySelectorAll('.text').forEach(el => el.style.display = 'inline');
                    row.querySelectorAll('.edit').forEach(el => el.style.display = 'none');
                    row.querySelector('.editBtn').style.display = 'inline';
                    btn.style.display = 'none';
                } else {
                    alert("Fehler beim Speichern!");
                }
            }).catch(err => {
                console.error(err);
                alert("Fehler beim Speichern!");
            });
        });
    });

    // Enter zum Speichern, Escape zum Abbrechen
    document.querySelectorAll('tr[data-id]').forEach(row => {
        row.querySelectorAll('input').forEach(input => {
            input.addEventListener('keydown', e => {
                if(e.key === 'Enter') row.querySelector('.saveBtn').click();
                if(e.key === 'Escape') {
                    row.querySelectorAll('.text').forEach(el => el.style.display='inline');
                    row.querySelectorAll('.edit').forEach(el => el.style.display='none');
                    row.querySelector('.editBtn').style.display='inline';
                    row.querySelector('.saveBtn').style.display='none';
                }
            });
        });
    });

});
