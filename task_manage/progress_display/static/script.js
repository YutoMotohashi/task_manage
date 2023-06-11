// Global variables
let currentData = null;
let selectedNode = null;

function fetchData() {
    fetch('/get_data')
        .then(response => response.json())
        .then(data => {
            currentData = data;
            displayDataInSidebar(data);
        });
}

function createNodeElement(node) {
    const nodeElement = document.createElement('div');
    nodeElement.className = 'node';
    nodeElement.setAttribute('data-number', node.number); // Add the number attribute

    const contentElement = document.createElement('span');
    contentElement.textContent = node.name;

    nodeElement.appendChild(contentElement);

    nodeElement.addEventListener('click', function (event) {
        event.stopPropagation(); // Prevent event propagation

        selectNode(node, nodeElement);
    });

    if (node.children && node.children.length > 0) {
        const childListElement = document.createElement('div');
        childListElement.className = 'child-list';

        for (let childNode of node.children) {
            const childNodeElement = createNodeElement(childNode);
            childListElement.appendChild(childNodeElement);
        }

        nodeElement.appendChild(childListElement);
    }

    return nodeElement;
}

function displayDataInSidebar(data) {
    const sidebarElement = document.getElementById('sidebar');
    sidebarElement.textContent = '';

    for (let node of data) {
        const nodeElement = createNodeElement(node);
        sidebarElement.appendChild(nodeElement);
    }
}

function selectNode(node, nodeElement) {
    if (selectedNode) {
        selectedNode.classList.remove('selected');
    }

    selectedNode = nodeElement;
    selectedNode.classList.add('selected');

    const form = document.getElementById('nodeForm');
    form.number.value = node.number;
    form.name.value = node.name;
    form.progress.value = node.progress;
    form.comment.value = node.comment;
    form.category.value = node.category;
    form.summary.value = node.summary;
    form.todo.value = node.todo;

    // Update the displayed progress value in the progress bar
    const progressBar = document.getElementById('progress');
    progressBar.value = node.progress;
    progressBar.textContent = `${node.progress}%`;

    // Update the displayed progress value in the form
    const progressValue = document.getElementById('progressValue');
    progressValue.textContent = `${node.progress}%`;

    const newChildNumberField = document.getElementById('newChildNumber'); // Get the new child number field
    newChildNumberField.placeholder = node.number + ".x"; // ".x" indicates the user should add a number here
}

document.getElementById('saveBtn').addEventListener('click', function () {
    if (selectedNode) {
        const form = document.getElementById('nodeForm');
        const progressValue = parseFloat(form.progress.value); // Convert to float

        selectedNode.dataset.progress = progressValue;
        selectedNode.dataset.name = form.name.value;
        selectedNode.dataset.comment = form.comment.value;
        selectedNode.dataset.summary = form.summary.value;
        selectedNode.dataset.todo = form.todo.value;

        // Update the data in the currentData variable
        updateData(selectedNode, form, currentData);

        // Save the updated data to the server
        saveDataToServer(currentData)
            .then(() => fetchData());
    }
});

document.getElementById('cancelBtn').addEventListener('click', function () {
    if (selectedNode) {
        document.getElementById('progress').value = selectedNode.dataset.progress;
        document.getElementById('comment').value = selectedNode.dataset.comment;
        document.getElementById('summary').value = selectedNode.dataset.summary;
        document.getElementById('todo').value = selectedNode.dataset.todo;
    }
});

// Category hierarchy
const categoryHierarchy = {
    'overall': 'chapter',
    'chapter': 'section',
    'section': 'subsection',
    'subsection': 'subsubsection'
};

// Checks if a given number is unique in the data set
function isNumberUnique(data, number) {
    for (let node of data) {
        if (node.number === number) {
            return false;
        }

        if (node.children && node.children.length > 0) {
            const isUniqueInChildren = isNumberUnique(node.children, number);
            if (!isUniqueInChildren) {
                return false;
            }
        }
    }

    return true;
}

document.getElementById('addChildBtn').addEventListener('click', function () {
    if (selectedNode) {
        const form = document.getElementById('nodeForm');
        const newChildName = document.getElementById('newChildName').value;
        const newChildNumber = document.getElementById('newChildNumber').value; // Get the new child number

        // Validate input number
        if (newChildNumber === '') {
            alert('Please enter a number for the new child node.');
            return;
        }

        if (!isNumberUnique(currentData, newChildNumber)) {
            alert('The number is not unique. Please enter a unique number.');
            return;
        }

        // Validate input name
        if (newChildName === '') {
            alert('Please enter a name for the new child node.');
            return;
        }

        const currentNode = findNodeByNumber(currentData, selectedNode.dataset.number);
        if (currentNode) {
            // Determine the category of the new child node based on the category of the current node
            const newChildCategory = categoryHierarchy[currentNode.category];

            // Create new child node
            const newChildNode = {
                number: newChildNumber, // Use the provided number
                name: newChildName,
                progress: 0,
                comment: '',
                category: newChildCategory,
                summary: '',
                todo: ''
            };

            if (!currentNode.children) {
                currentNode.children = [];
            }
            currentNode.children.push(newChildNode);
        }

        // Save the updated data to the server
        // and Fetch new data from the server to update the UI
        saveDataToServer(currentData)
            .then(() => fetchData());


        // Clear the new child name and number inputs
        document.getElementById('newChildName').value = '';
        document.getElementById('newChildNumber').value = '';
    }
});

function updateData(node, form, data) {
    if (!node) {
        return;
    }

    const nodeNumber = node.dataset.number;
    const currentNode = findNodeByNumber(data, nodeNumber);
    if (currentNode) {
        currentNode.progress = form.progress.value;
        currentNode.name = form.name.value;
        currentNode.comment = form.comment.value;
        currentNode.summary = form.summary.value;
        currentNode.todo = form.todo.value;
    }

    if (node.children && node.children.length > 0) {
        for (let childNode of node.children) {
            const childElement = document.querySelector(`.node[data-number="${childNode.number}"]`);
            updateData(childElement, form, data);
        }
    }
}

function findNodeByNumber(data, number) {
    for (let node of data) {
        if (node.number === number) {
            return node;
        }

        if (node.children && node.children.length > 0) {
            const foundNode = findNodeByNumber(node.children, number);
            if (foundNode) {
                return foundNode;
            }
        }
    }

    return null;
}

function saveDataToServer(data) {
    return fetch('/save_data', {  // notice the 'return' here
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(responseData => {
            console.log('Data saved successfully:', responseData);
        })
        .catch(error => {
            console.error('Error saving data:', error);
        });
}
fetchData();