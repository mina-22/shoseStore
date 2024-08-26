
let icons = document.querySelector(".fav-icon");


icons.addEventListener("click", function () {

        if (icons.classList.contains("fav-color")) {
        let productId = +(icons.getAttribute("productIdCustom"));
        let id = +(icons.getAttribute("cancelo"));

            let FavUser =
            {
                ProductId: productId,
                Id: id

            };

            $.ajax({
            url: @Url.Action("RemoveFav", "Select"),
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(FavUser),
                success: function () {
                icons.classList.remove("fav-color");
                icons.classList.remove("fas");
                icons.classList.add("far");
                }
            })
        }
        else {
        let productId = +(icons.getAttribute("productIdCustom"));

            let FavUser =
            {
                ProductId: productId,
                Id: 0
            };

            $.ajax({
            url: @Url.Action("AddFav", "Select"),
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(FavUser),
                success: function () {
                icons.classList.add("fav-color");
                icons.classList.add("fas");
                icons.classList.remove("far");
                }
            })
        }
    });