<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Manager Dashboard</a>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="nav-link active" href="#">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click="exportdata">Export CSV</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click="logout">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-10">

        <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

        <div class="card mb-4">
          <div class="card-header">Add New Product</div>
          <div class="card-body">
            <div class="row g-2">
              <div class="col-md-4">
                <input type="text" class="form-control" placeholder="Name" v-model="newProduct.name">
              </div>
              <div class="col-md-4">
                <input type="text" class="form-control" placeholder="Description" v-model="newProduct.description">
              </div>
              <div class="col-md-4">
                <input type="number" class="form-control" placeholder="Price" v-model="newProduct.price">
              </div>
              <div class="col-md-4">
                <input type="text" class="form-control" placeholder="Unit" v-model="newProduct.unit">
              </div>
              <div class="col-md-4">
                <input type="number" class="form-control" placeholder="Stock" v-model="newProduct.stock">
              </div>
              <div class="col-md-4">
                <select class="form-control" v-model="newProduct.category_id">
                  <option value="">Select Category</option>
                  <!-- FIX 5 (partial): renamed loop var to 'cat' here too for consistency -->
                  <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                    {{ cat.name }}
                  </option>
                </select>
              </div>
              <div class="col-md-12">
                <button class="btn btn-success" @click="addProduct">Add Product</button>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">All Products</div>
          <div class="card-body">
            <table v-if = "allProducts !=0" class="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Price</th>
                  <th>Unit</th>
                  <th>Stock</th>
                  <th>Category</th>
                  <th>Delete</th>
                  <th>Edit</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="product in allProducts" :key="product.id">
                  <td>{{ product.id }}</td>
                  <td>{{ product.name }}</td>
                  <td>{{ product.price }}</td>
                  <td>{{ product.unit }}</td>
                  <td>{{ product.stock }}</td>
                  <td>{{ product.category_name }}</td>
                  <td>
                    <button class="btn btn-danger btn-sm" @click="deleteProduct(product.id)">Delete</button>
                  </td>
                  <td>
                    <button class="btn btn-primary btn-sm" @click="editProduct(product.id)">Edit</button>
                  </td>
                </tr>
              </tbody>
            </table>
            <p v-else>No Products Found</p>
          </div>
        </div>

      </div>
    </div>
  </div>

  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-10">
        <!-- FIX 1: card-body is now properly inside the card div -->
        <div class="card">
          <div class="card-header">Manage Category</div>
          <div class="card-body">
            <!-- FIX 2: corrected method name to SendCreateUpdateDeleteRequest -->
            <form @submit.prevent="SendCreateUpdateDeleteRequest(categoryrequest.action)">
              <div class="form-group">
                <label for="action">Action</label>
                <!-- FIX 3: bind to categoryrequest.action -->
                <select class="form-control" id="action" v-model="categoryrequest.action">
                  <option value="CREATE">Create</option>
                  <option value="UPDATE">Update</option>
                  <option value="DELETE">Delete</option>
                </select>
              </div>

              <!-- FIX 4: was category.action, now categoryrequest.action -->
              <div v-if="categoryrequest.action !== 'CREATE'" class="form-group">
                <label for="category">Select Category</label>
                <!-- FIX 5: renamed loop variable to 'cat' to avoid shadowing -->
                <select class="form-select" id="category" v-model="categoryrequest.category_id">
                  <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                </select>
              </div>

              <div v-if="categoryrequest.action !== 'DELETE'" class="form-group">
                <label for="name">Name</label>
                <input type="text" class="form-control" id="name" v-model="categoryrequest.name" required>
              </div>

              <button type="submit" class="btn btn-primary">Submit</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-10">
        <div class="card">
          <div class="card-header">Category Request</div>
          <div class="card-body">
            <table v-if = "categoryRequest !=0" class="table">
              <thead>
                <tr>
                  <th scope="col">Category ID</th>
                  <th scope="col">Name</th>
                  <th scope="col">Action</th>
                  <th scope="col">Status</th>
                </tr>
              </thead>
              <tbody>
                <!-- FIX 6: iterate over categoryRequest, not categories -->
                <tr v-for="(request, index) in categoryRequest" :key="index">
                  <td>{{ request.category_id }}</td>
                  <td>{{ request.name }}</td>
                  <td>{{ request.action }}</td>
                  <td>{{ request.status }}</td>
                </tr>
              </tbody>
            </table>
            <p if-else>No Request Found</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      allProducts: [],
      categories: [],
      errorMessage: '',
      newProduct: {
        name: '',
        description: '',
        price: '',
        unit: '',
        stock: '',
        category_id: '',
      },
      categoryrequest: {
        action: 'CREATE',
        category_id: '',
        name: '',
      },
      categoryRequest: [],
    };
  },
  methods: {
    async logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    },
    async exportdata() {
      try {
        const response = await fetch('/api/product/export', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          const result = await response.json();
          alert(result.message);
        } else {
          const result = await response.json();
          alert(result.message);
        }
      } catch (error) {
        alert("Unable to connect to the server");
      }
    },
    async SendCreateUpdateDeleteRequest(action) {
    try {
        const response = await fetch('/api/category/request', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: action,
                category_id: action !== 'CREATE' ? this.categoryrequest.category_id : undefined,
                name: action !== 'DELETE' ? this.categoryrequest.name : undefined,
            }),
        });
        const result = await response.json();
        console.log('POST result:', result); // ADD THIS
        if (!response.ok) {
            alert(result.message || "Error submitting category request");
        } else {
            alert("Category request submitted successfully");
            this.categoryrequest = { action: 'CREATE', category_id: '', name: '' };
            await this.fetchCategoryRequest(); // await it so it finishes before anything else
        }
    } catch (error) {
        console.error('Submit error:', error); // ADD THIS
        alert("Unable to connect to the server");
    }
},
    async fetchCategoryRequest() {
    try {
        const response = await fetch('/api/category/request', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
        });
        const result = await response.json();
        if (!response.ok) {
            this.errorMessage = result.message || "Error fetching category requests";
        } else {
            // FIX: extract the array from the correct key
            this.categoryRequest = result.category_request;
        }
    } catch (error) {
        this.errorMessage = "Unable to connect to the server";
    }
},

    async fetchProducts() {
      try {
        const response = await fetch('/api/product', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
        });
        const result = await response.json();
        if (!response.ok) {
          this.errorMessage = result.message || "Error fetching products";
        } else {
          this.allProducts = result.products;
        }
      } catch (error) {
        this.errorMessage = "Unable to connect to the server";
      }
    },

    async fetchCategories() {
      try {
        const response = await fetch('/api/category', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
        });
        const result = await response.json();
        if (!response.ok) {
          this.errorMessage = result.message || "Error fetching categories";
        } else {
          this.categories = result;
        }
      } catch (error) {
        this.errorMessage = "Unable to connect to the server";
      }
    },

    async addProduct() {
      try {
        const response = await fetch('/api/product', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: this.newProduct.name,
            description: this.newProduct.description,
            price: this.newProduct.price,
            unit: this.newProduct.unit,
            stock: this.newProduct.stock,
            category_id: this.newProduct.category_id,
          }),
        });
        const result = await response.json();
        if (!response.ok) {
          this.errorMessage = result.message || "Something went wrong";
        } else {
          alert("Product added successfully");
          this.newProduct = { name: '', description: '', price: '', unit: '', stock: '', category_id: '' };
          this.fetchProducts();
        }
      } catch (error) {
        this.errorMessage = "Unable to connect to the server";
      }
    },

    async deleteProduct(id) {
      try {
        const response = await fetch(`/api/product/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          alert("Product deleted successfully");
          this.fetchProducts();
        } else {
          const result = await response.json();
          alert(result.message || "Error deleting product");
        }
      } catch (error) {
        alert("Unable to connect to the server");
      }
    },

    editProduct(id) {
      this.$router.push(`/edit-product/${id}`);
    },
  },

  mounted() {
    this.fetchProducts();
    this.fetchCategories();
    this.fetchCategoryRequest();
  },
}
</script>