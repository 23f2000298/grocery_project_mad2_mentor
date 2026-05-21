<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">User Signup</div>
                    <div class="card-body">
                        <form @submit.prevent="signupUser">
                            <div class="form-group">
                                <label for="name">Name</label>
                                <input type="text" class="form-control" id="name" v-model="name" required>
                            </div>
                            <div class="form-group">
                                <label for="email">Email</label>
                                <input type="email" class="form-control" id="email" v-model="email" required>
                            </div>
                            <div class="form-group">
                                <label for="password">Password</label>
                                <input type="password" class="form-control" id="password" v-model="password" required>
                            </div>
                            <div v-if="error" class="alert alert-danger" role="alert">
                                {{ error }}
                            </div>
                            <div v-if="success" class="alert alert-success" role="alert">
                                {{ success }}
                            </div>
                            <button type="submit" class="btn btn-primary">Signup</button>
                            <router-link to="/user-login" class="btn btn-secondary ms-2">Login</router-link>
                        </form>
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
            name: '',
            email: '',
            password: '',
            error: null,
            success: null
        }
    },
    methods: {
        async signupUser() {
            this.error = null;
            this.success = null;
            const payload = {
                name: this.name,
                email: this.email,
                password: this.password,
                role: "customer"
            };
            try {
                const response = await fetch('/api/signup', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });
                const result = await response.json();
                if (!response.ok) {
                    this.error = result.message || "Something went wrong";
                } else {
                    this.success = "Signup successful!";
                    setTimeout(() => this.$router.push('/user-login'), 1500);
                }
            } catch(error) {
                this.error = "Unable to connect to the server";
            }
        }
    }
}
</script>