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

    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-10">
                <div class="card">
                    <div class="card-header">Your Cart</div>
                    <div class="card-body">
                        <p v-if="cart.length === 0" class="text-center">Your cart is empty.</p>
                        <table v-else class="table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Price</th>
                                    <th>Unit</th>
                                    <th>Quantity</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="product in cart" :key="product.id">
                                    <td>{{ product.product_name }}</td>
                                    <td>{{ product.product_price }}</td>
                                    <td>{{ product.product_unit }}</td>
                                    <td>{{ product.quantity }}</td>
                                    <td>
                                        <!-- ✅ pass -1 or +1 as delta -->
                                        <button @click="updateQuantity(product.id, -1)" class="btn btn-sm btn-danger">-</button>
                                        <button @click="updateQuantity(product.id, 1)" class="btn btn-sm btn-success">+</button>
                                        <button @click="deleteCart(product.id)" class="btn btn-sm btn-warning ms-1">🗑</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div class="text-center mt-3">
                            <h4>Total: ₹{{ total }}</h4>
                            <button class="btn btn-primary" @click="Ordernow">Order Now</button>
                        </div>
                    </div>
                </div>
                <div class="mt-2">
                    <router-link to="/customer" class="btn btn-warning">Continue Shopping</router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            cart: [],
            total: 0,
        };
    },
    // ✅ mounted at component level, NOT inside methods
    mounted() {
        this.fetchCart();
    },
    methods: {
        async logout() {
            localStorage.removeItem('token');
            this.$router.push('/');
        },
        async fetchCart() {
            try {
                const response = await fetch('/api/cart', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json',
                    },
                });
                if (response.ok) {
                    const result = await response.json();
                    this.cart = result.cart;
                    this.total = result.total;
                } else {
                    alert("Error fetching cart");
                }
            } catch (error) {
                alert("Unable to connect to the server");
            }
        },
        async Ordernow() {
        try {
            const response = await fetch('/api/order', {  // ✅ fixed URL
                method: 'POST',
                headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json',
                    },
                });
                const result = await response.json();  // ✅ moved outside if/else
                if (response.ok) {
                    alert("Order placed successfully");
                    this.$router.push('/customer/orders');
                } else {
                    alert(result.message || "Error placing order");
                }
            } catch (error) {
                alert("Unable to connect to the server");
            }
        },
        async updateQuantity(id, delta) {
            try {
                const response = await fetch(`/api/cart/${id}`, {
                    method: 'PATCH', // ✅ was PUT, backend uses PATCH
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ quantity: delta }), // ✅ send -1 or +1
                });
                if (response.ok) {
                    const result = await response.json();
                    alert("Quantity updated successfully");
                    await this.fetchCart(); // ✅ refresh without alert spam
                } else {
                    alert(result.message || "Error updating quantity");
                }
            } catch (error) {
                alert("Unable to connect to the server");
            }
        },
        async deleteCart(id) {
            try {
                const response = await fetch(`/api/cart/${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json',
                    },
                });
                if (response.ok) {
                    await this.fetchCart(); // ✅ refresh cart
                } else {
                    const result = await response.json();
                    alert(result.message || "Error deleting product");
                }
            } catch (error) {
                alert("Unable to connect to the server");
            }
        },
        async checkout() {
            // wire up to your PurchaseAPI when ready
            alert("Checkout coming soon!");
        }
    }
}
</script>