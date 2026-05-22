<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">Create Category</div>
                    <div class="card-body">
                        <form @submit.prevent="createCategory">
                            <div class="form-group">
                                <label for="name">Name</label>
                                <input type="text" class="form-control" id="name" v-model="name" required>
                            </div>
                            <div v-if="error" class="alert alert-danger" role="alert">
                                {{ error }}
                            </div>
                            <div v-if="success" class="alert alert-success" role="alert">
                                {{ success }}
                            </div>
                            <button type="submit" class="btn btn-primary">Create</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>  <!-- this was missing -->
</template>

<script>
export default {
    data() {
        return {
            name: '',
            description: '',
            error: null,
            success: null
        };
    },
    methods: {
        async createCategory() {
            this.error = null;
            this.success = null;
            const payload = {
                name: this.name,
                description: this.description
            };
            try {
                const response = await fetch('/api/category', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });
                const result = await response.json();
                if (!response.ok) {
                    this.error = result.message || "Something went wrong";
                } else {
                    this.success = "Category created successfully!";
                    setTimeout(() => this.$router.push('/admin'), 1500);
                }
            } catch(error) {
                this.error = "Unable to connect to the server";
            }
        }
    }
};
</script>