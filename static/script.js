document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("food-modal");
    const closeButton = document.getElementById("close-modal");
    const addItemButton = document.getElementById("add-item-btn");
    const foodForm = document.getElementById("food-form");
    const foodList = document.getElementById("food-list");
    const modalTitle = document.getElementById("modal-title");
// TOM SELECT/SEARCH DROPDOWN(BOTH)
    new TomSelect("#food-name", {
        create: false
    });

    new TomSelect("#edit-food-select", {
        create: false
    });

    const customFoodBtn =
      document.getElementById(
         "add-custom-food-btn"
      );

   const customFoodForm =
      document.getElementById(
         "custom-food-form"
      );

   const customItemBtn =
      document.getElementById(
         "add-custom-item-btn"
      );

   const customItemForm =
      document.getElementById(
         "custom-item-form"
      );

    const editItemBtn =
      document.getElementById(
         "edit-item-btn"
      );

const editItemForm =
      document.getElementById(
         "edit-item-form"
      );


    let selectedCell = null;
    let editingFoodId = null;

    // Temporary storage
    const cellFoods = {};
    window.cellFoods = cellFoods;
    SAVED_FOODS.forEach(food => {

         const [
            id,
            date,
            slot,
            foodName,
            quantity,
            unit,
            fdc_id,
            calories,
            protein,
            carbs,
            fat,
            fiber,
            sugar,
            sodium
         ] = food;

         const key = `${date}_${slot}`;

         if (!cellFoods[key]) {
            cellFoods[key] = [];
         }

         cellFoods[key].push({
            id: id,
            name: foodName,
            quantity: quantity,
            unit: unit,
            fdc_id: fdc_id,
            calories: calories,
            protein: protein,
            carbs: carbs,
            fat: fat
         });

      });

    function getCellKey(cell) {

        const date = cell.dataset.date;
        const slot = cell.dataset.slot;

        return `${date}_${slot}`;
    }

    function renderFoodList(cell) {

        const key = getCellKey(cell);

        foodList.innerHTML = "";

        if (!cellFoods[key]) {
            cellFoods[key] = [];
        }

        cellFoods[key].forEach(food => {

            const div = document.createElement("div");

            const text = document.createElement("span");

            if (food.unit === "count") {

               text.textContent =
                  `${food.name} (${food.quantity})`;

            } else {

               text.textContent =
                  `${food.name} (${food.quantity}${food.unit})`;

            }

            const editBtn =
               document.createElement("button");

            editBtn.textContent = "Edit";

            editBtn.addEventListener("click", () => {

               editingFoodId = food.id;

               document.getElementById("food-name").value =
                  food.fdc_id;

               document.getElementById("food-quantity").value =
                  food.quantity;

               document.getElementById("food-unit").value =
                  food.unit;

               foodForm.style.display = "flex";

            });

            const deleteBtn =
               document.createElement("button");

            deleteBtn.addEventListener("click", () => {

               if (!confirm(`Delete ${food.name}?`)) {
                  return;
               }

               fetch("/delete-food", {
                  method: "POST",
                  headers: {
                     "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                     id: food.id
                  })
               })
               .then(response => {

                  console.log("STATUS:", response.status);

                  return response.text();

               })
               .then(data => {

                  console.log("RESPONSE:", data);

                  const index =
                     cellFoods[key].findIndex(
                        item => item.id === food.id
                     );

                  if (index !== -1) {
                     cellFoods[key].splice(index, 1);
                  }

                  window.location.reload();

               })
               .catch(error => {

                  console.error("DELETE FAILED:", error);

               });
               });

            deleteBtn.textContent = "Delete";

            div.appendChild(text);
            div.appendChild(editBtn);
            div.appendChild(deleteBtn);

            foodList.appendChild(div);

        });

    }
    
    function renderCell(cell) {

         const key = getCellKey(cell);

         const foods = cellFoods[key] || [];

         if (foods.length === 0) {

            cell.textContent = "+";

            return;

         }

         const visibleFoods =
            foods.slice(0, 3);

         let cellHtml =
            visibleFoods
                  .map(food => food.name)
                  .join("<br>");

         if (foods.length > 3) {

            cellHtml +=
                  `<br>+${foods.length - 3} more`;

         }

         cell.innerHTML = cellHtml;

      }

    document.querySelectorAll(".food-cell").forEach(cell => {

         renderCell(cell);

      });

    document.querySelectorAll(".food-cell").forEach(cell => {

        cell.addEventListener("click", () => {

            selectedCell = cell;

            foodForm.style.display = "none";
            customFoodForm.style.display = "none";
            customItemForm.style.display = "none";

            document.getElementById("recipe-items").innerHTML = "";
            document.getElementById("custom-item-name").value = "";

            modalTitle.textContent =
                `${cell.dataset.date} • ${cell.dataset.slot}`;

            foodForm.style.display = "none";

            customFoodForm.style.display = "none";

            renderFoodList(cell);

            modal.style.display = "flex";

        });

    });

    addItemButton.addEventListener("click", () => {

        customFoodForm.style.display = "none";
        customItemForm.style.display = "none";
        editItemForm.style.display = "none";

        foodForm.style.display = "flex";

    });

    customFoodBtn.addEventListener("click", () => {

      foodForm.style.display = "none";
      customItemForm.style.display = "none";
      editItemForm.style.display = "none";

      customFoodForm.style.display = "flex";

    });

    customItemBtn.addEventListener("click", () => {

      foodForm.style.display = "none";

      customFoodForm.style.display = "none";
      editItemForm.style.display = "none";

      customItemForm.style.display = "flex";

    });

    editItemBtn.addEventListener("click", () => {

        foodForm.style.display = "none";
        customFoodForm.style.display = "none";
        customItemForm.style.display = "none";

        editItemForm.style.display = "flex";

    });

    closeButton.addEventListener("click", () => {



        document.getElementById("custom-name").value = "";

        document.getElementById("custom-calories").value = "";
        document.getElementById("custom-protein").value = "";
        document.getElementById("custom-carbs").value = "";
        document.getElementById("custom-fat").value = "";
        document.getElementById("custom-fiber").value = "";
        document.getElementById("custom-sugar").value = "";
        document.getElementById("custom-sodium").value = "";
        document.getElementById("custom-serving-weight").value = "";
        document.getElementById("food-name").value = "";
        document.getElementById("food-quantity").value = "";
        document.getElementById("food-unit").selectedIndex = 0;
        document.getElementById("edit-food-name").value = "";
        document.getElementById("edit-calories").value = "";
        document.getElementById("edit-protein").value = "";
        document.getElementById("edit-carbs").value = "";
        document.getElementById("edit-fat").value = "";
        document.getElementById("edit-fiber").value = "";
        document.getElementById("edit-sugar").value = "";
        document.getElementById("edit-sodium").value = "";
        document.getElementById("edit-serving-weight").value = "";

        foodForm.style.display = "none";
        customFoodForm.style.display = "none";
        customItemForm.style.display = "none";
        editItemForm.style.display = "none";

        document.getElementById(
            "edit-food-select"
        ).selectedIndex = 0;

        document.getElementById(
            "edit-food-name"
        ).value = "";

        document.getElementById(
            "edit-calories"
        ).value = "";

        document.getElementById(
            "edit-protein"
        ).value = "";

        document.getElementById(
            "edit-carbs"
        ).value = "";

        document.getElementById(
            "edit-fat"
        ).value = "";

        document.getElementById(
            "edit-fiber"
        ).value = "";

        document.getElementById(
            "edit-sugar"
        ).value = "";

        document.getElementById(
            "edit-sodium"
        ).value = "";

        document.getElementById(
            "edit-serving-weight"
        ).value = "";

        document.getElementById("recipe-items").innerHTML = "";
        document.getElementById("custom-item-name").value = "";

        modal.style.display = "none";

    });

    document
        .getElementById("save-food")
        .addEventListener("click", () => {

            const foodSelect =
               document.getElementById("food-name");

            const foodName =
               foodSelect.options[
                  foodSelect.selectedIndex
               ].text;

            const quantity =
                document.getElementById("food-quantity").value;

            if (
                quantity.trim() === "" ||
                Number(quantity) <= 0
            ) {
                alert("Enter a valid quantity");
                return;
            }

            const unit =
                document.getElementById("food-unit").value;

            if (
                !selectedCell ||
                foodName.trim() === ""
            ) {
                return;
            }

            const key = getCellKey(selectedCell);

            if (!cellFoods[key]) {
               cellFoods[key] = [];
            }

            if (editingFoodId !== null) {

               const foodToEdit =
                  cellFoods[key].find(
                        item => item.id === editingFoodId
                  );

               if (foodToEdit) {

                  foodToEdit.name = foodName;
                  foodToEdit.quantity = quantity;
                  foodToEdit.unit = unit;

               }

               fetch("/update-food", {
                  method: "POST",
                  headers: {
                        "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                        id: editingFoodId,
                        food_name: foodName,
                        quantity: quantity,
                        unit: unit,
                        fdc_id: foodSelect.value
                  })
               })

               .then(response => response.json())
               .then(data => {

                  window.location.reload();

               });

               editingFoodId = null;

            } else {

               cellFoods[key].push({
                  name: foodName,
                  quantity: quantity,
                  unit: unit
               });

               fetch("/add-food", {
                  method: "POST",
                  headers: {
                     "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                     date: selectedCell.dataset.date,
                     slot: selectedCell.dataset.slot,
                     food_name: foodName,
                     quantity: quantity,
                     unit: unit,
                     fdc_id: foodSelect.value
                  })
               })
               .then(response => response.json())
               .then(data => {

                  window.location.reload();

               });

            }

            renderFoodList(selectedCell);

            // Update cell display

            const foods = cellFoods[key];

            renderCell(selectedCell);

            document.getElementById("food-name").value = "";
            document.getElementById("food-quantity").value = "";
            document.getElementById("food-unit").selectedIndex = 0;

            foodForm.style.display = "none";

        });
document
.getElementById("save-custom-food")
.addEventListener("click", () => {

    console.log("SAVE CUSTOM FOOD CLICKED");
    console.log({

      display_name:
         document.getElementById(
               "custom-name"
         ).value,

      calories:
         document.getElementById(
               "custom-calories"
         ).value,

      protein:
         document.getElementById(
               "custom-protein"
         ).value,

      carbs:
         document.getElementById(
               "custom-carbs"
         ).value,

      fat:
         document.getElementById(
               "custom-fat"
         ).value,

      fiber:
         document.getElementById(
               "custom-fiber"
         ).value,

      sugar:
         document.getElementById(
               "custom-sugar"
         ).value,

      sodium:
         document.getElementById(
               "custom-sodium"
         ).value,

      serving_weight:
         document.getElementById(
               "custom-serving-weight"
         ).value

    });
    fetch("/add-custom-food", {

        method: "POST",

        headers: {
            "Content-Type":
                "application/json"
        },

        body: JSON.stringify({

            display_name:
                document.getElementById(
                    "custom-name"
                ).value,

            calories:
                document.getElementById(
                    "custom-calories"
                ).value,

            protein:
                document.getElementById(
                    "custom-protein"
                ).value,

            carbs:
                document.getElementById(
                    "custom-carbs"
                ).value,

            fat:
                document.getElementById(
                    "custom-fat"
                ).value,

            fiber:
                document.getElementById(
                    "custom-fiber"
                ).value,

            sugar:
                document.getElementById(
                    "custom-sugar"
                ).value,

            sodium:
                document.getElementById(
                    "custom-sodium"
                ).value,

            serving_weight:
                document.getElementById(
                    "custom-serving-weight"
                ).value

        })

    })

    .then(response => response.json())

    .then(data => {

        window.location.reload();

    });

});


document
.getElementById("add-recipe-item")
.addEventListener("click", () => {

    const row =
        document.createElement("div");

    let options = `

        <option value="" selected>

            Select Food

        </option>

    `;

    APP_FOODS.forEach(food => {

        options += `
            <option value="${food[0]}">
                ${food[1]}
            </option>
        `;

    });

    row.innerHTML = `

        <select class="recipe-food">
            ${options}
        </select>

        <input
            type="number"
            class="recipe-qty"
            placeholder="Qty"
        >

        <select class="recipe-unit">
            <option>g</option>
            <option>ml</option>
            <option>count</option>
        </select>

    `;

    document
        .getElementById("recipe-items")
        .appendChild(row);
    
    // new TomSelect(
    //     row.querySelector(".recipe-food"),
    //     {
    //         create: false
    //     }
    // );

});




document
.getElementById("save-custom-item")
.addEventListener("click", () => {

    const recipeName =
        document.getElementById(
            "custom-item-name"
        ).value;

    if (recipeName.trim() === "") {
        alert("Enter a recipe name");
        return;
    }

    const items = [];

    let hasInvalidQuantity = false;

    document
    .querySelectorAll("#recipe-items > div")
    .forEach(row => {

        const qty =
            row.querySelector(".recipe-qty").value;

        if (
            qty.trim() === "" ||
            Number(qty) <= 0
        ) {
            hasInvalidQuantity = true;
            return;
        }

        items.push({

            fdc_id:
                parseInt(
                    row.querySelector(".recipe-food").value
                ),

            quantity:
                parseFloat(qty),

            unit:
                row.querySelector(".recipe-unit").value

        });

    });

    if (hasInvalidQuantity) {
        alert("All ingredients must have a quantity greater than 0");
        return;
    }

    if (items.length === 0) {
        alert("Add at least one ingredient");
        return;
    }

    fetch("/save-custom-item", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            name: recipeName,
            items: items

        })

    })

    .then(response => response.json())

    .then(data => {

        window.location.reload();

    });

});


document
.getElementById("delete-food-master")
.addEventListener("click", () => {

    const foodSelect =
        document.getElementById("food-name");

    const foodName =
        foodSelect.options[
            foodSelect.selectedIndex
        ].text;

    if (
        !confirm(
            `Delete "${foodName}" permanently?`
        )
    ) {
        return;
    }

    fetch("/delete-app-food", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            fdc_id: foodSelect.value

        })

    })

    .then(response => response.json())

    .then(data => {

        if (!data.success) {

            alert(data.message);

            return;

        }

        alert("Food deleted");

        window.location.reload();

    });

});


document
.getElementById("load-food")
.addEventListener("click", () => {

    const fdcId =
        document.getElementById(
            "edit-food-select"
        ).value;

    fetch(`/food/${fdcId}`)

    .then(response => response.json())

    .then(food => {

        document.getElementById(
            "edit-food-name"
        ).value = food.food_name;

        document.getElementById(
            "edit-calories"
        ).value = food.calories;

        document.getElementById(
            "edit-protein"
        ).value = food.protein;

        document.getElementById(
            "edit-carbs"
        ).value = food.carbs;

        document.getElementById(
            "edit-fat"
        ).value = food.fat;

        document.getElementById(
            "edit-fiber"
        ).value = food.fiber;

        document.getElementById(
            "edit-sugar"
        ).value = food.sugar;

        document.getElementById(
            "edit-sodium"
        ).value = food.sodium;

        document.getElementById(
            "edit-serving-weight"
        ).value = food.serving_weight;

    });

});


document
.getElementById("save-edit-food")
.addEventListener("click", () => {

    const fdcId =
        document.getElementById(
            "edit-food-select"
        ).value;

    if (

        !confirm(

            "Save changes to this food?"

        )

    ) {

        return;

    }

    fetch("/update-app-food", {

        method: "POST",

        headers: {
            "Content-Type":
                "application/json"
        },

        body: JSON.stringify({

            fdc_id: fdcId,

            food_name:
                document.getElementById(
                    "edit-food-name"
                ).value,

            calories:
                document.getElementById(
                    "edit-calories"
                ).value,

            protein:
                document.getElementById(
                    "edit-protein"
                ).value,

            carbs:
                document.getElementById(
                    "edit-carbs"
                ).value,

            fat:
                document.getElementById(
                    "edit-fat"
                ).value,

            fiber:
                document.getElementById(
                    "edit-fiber"
                ).value,

            sugar:
                document.getElementById(
                    "edit-sugar"
                ).value,

            sodium:
                document.getElementById(
                    "edit-sodium"
                ).value,

            serving_weight:
                document.getElementById(
                    "edit-serving-weight"
                ).value

        })

    })

    .then(response => response.json())

    .then(data => {

        alert("Food updated");

        window.location.reload();

    });

});
});





