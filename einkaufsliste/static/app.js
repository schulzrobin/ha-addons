document.querySelectorAll('.editBtn').forEach(btn => {
    btn.onclick = () => {
        const row = btn.closest('tr');
        row.querySelectorAll('.text').forEach(e => e.hidden = true);
        row.querySelectorAll('.edit').forEach(e => e.hidden = false);
        btn.hidden = true;
        row.querySelector('.saveBtn').hidden = false;
    };
});

document.querySelectorAll('.saveBtn').forEach(btn => {
    btn.onclick = () => {
        const row = btn.closest('tr');
        const id = row.dataset.id;
        const inputs = row.querySelectorAll('.edit');

        fetch(`/update/${id}`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                menge: inputs[0].value,
                einheit: inputs[1].value,
                artikel: inputs[2].value
            })
        }).then(() => location.reload());
    };
});