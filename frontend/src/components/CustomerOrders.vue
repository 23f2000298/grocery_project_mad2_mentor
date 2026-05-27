
<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Customer Dashboard</a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <router-link to="/customer" class="nav-link">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/customer/cart" class="nav-link">Cart</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/customer/orders" class="nav-link">Orders</router-link>
                    </li>
                </ul>
                <button class="btn btn-danger" @click="logout">Logout</button>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class = "row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">Orders</div>
                    <div class="card-body">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">Order No.</th>
                                    <th scope="col">Product Name</th>
                                    <th scope="col">Quantity</th>
                                    <th scope="col">Price</th>
                                    <th scope="col">Unit</th>
                                    <th scope="col">Description</th>
                                    <th scope="col">Date of Purchase</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="order in orders" :key="order.id">
                                    <th scope="row">{{ order.id }}</th>
                                    <td>{{ order.product_name }}</td>
                                    <td>{{ order.quantity }}</td>
                                    <td>{{ order.product_price }}</td>        <!-- ✅ was order.price -->
                                    <td>{{ order.product_unit }}</td>         <!-- ✅ was order.unit -->
                                    <td>{{ order.product_description }}</td>  <!-- ✅ was order.description -->
                                    <td>{{ order.date_of_purchase }}</td>  
                                </tr>
                            </tbody>
                        </table>
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
            orders: []
        }
    },
    mounted() {
        this.fetchOrders()
    },
    methods: {
        async logout() {
            localStorage.removeItem('token');
            this.$router.push('/');
        },
        async fetchOrders() {
            try {
                const response = await fetch('/api/order', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        "Content-Type": "application/json"
                    }
                });
                if (response.ok) {
                    const result = await response.json();
                    this.orders = result.orders;
                } else {
                    alert("Error fetching orders");
                }
            } catch (error) {
                alert("Unable to connect to the server");
            }
        },
        mounted(){
            this.fetchOrders();
        }

    },
};
</script>
