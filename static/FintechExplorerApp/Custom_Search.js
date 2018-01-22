    function check_event() {
        var switcher = document.getElementById('myonoffswitch');
        if (switcher.checked) {
            document.getElementById('QueryTypeID').value = "name"
        }
        else {
            document.getElementById('QueryTypeID').value = "content"
        }
    }

    function check_reset() {
        document.getElementById('myonoffswitch').checked = true;
        document.getElementById('QueryTypeID').value = "name";
    }