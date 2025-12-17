document.addEventListener("DOMContentLoaded", () => {
    const rows = document.querySelectorAll(".product-row");

    rows.forEach(row => {
        row.addEventListener("click", () => {
            // Remove "selected" class from any previously selected row
            document.querySelectorAll(".product-row.selected").forEach(r => r.classList.remove("selected"));

            // Add "selected" class to clicked row
            row.classList.add("selected");

            // Get product data
            const leaflet = row.dataset.leaflet;
            const name = row.dataset.name;
            const price = row.dataset.price;

            const productData = { leaflet, name, price };
            console.log("Selected product:", productData);

            // Send selection to Flask endpoint
            fetch("/select_product", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(productData)
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === "success"){
                    // Show a temporary success message
                    showMessage(`Product selected: ${name} - ${price}`);
                } else {
                    showMessage("Failed to save selection.", true);
                }
            });
        });
    });

    // Function to show temporary message
    function showMessage(msg, isError = false) {
        let div = document.getElementById("message-box");
        if(!div) {
            div = document.createElement("div");
            div.id = "message-box";
            div.style.position = "fixed";
            div.style.top = "10px";
            div.style.right = "10px";
            div.style.padding = "10px 20px";
            div.style.borderRadius = "5px";
            div.style.color = "#fff";
            div.style.fontWeight = "bold";
            div.style.zIndex = "1000";
            document.body.appendChild(div);
        }

        div.textContent = msg;
        div.style.backgroundColor = isError ? "#e74c3c" : "#27ae60";

        // Hide after 3 seconds
        setTimeout(() => div.textContent = "", 3000);
    }
});
