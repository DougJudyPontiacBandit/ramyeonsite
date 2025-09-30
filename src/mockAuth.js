// Mock Authentication Service
// This provides a working authentication system using localStorage
// while the backend is being fixed

class MockAuthService {
  constructor() {
    this.users = this.loadUsers();
  }

  loadUsers() {
    const stored = localStorage.getItem('mock_users');
    if (stored) {
      return JSON.parse(stored);
    }
    
    // Default test users
    return [
      {
        id: 'USER-001',
        email: 'test@ramyeoncorner.com',
        password: 'Test123!', // In real app, this would be hashed
        first_name: 'Test',
        last_name: 'User',
        phone: '+1234567890',
        role: 'customer',
        status: 'active',
        points: 3280,
        vouchers: [
          {
            id: 1,
            title: 'Shin Ramyun',
            subtitle: 'Spicy Noodle',
            discount: '20% OFF',
            code: 'SHIN20',
            qrCode: 'SHIN20-QR-' + Date.now()
          }
        ],
        date_created: new Date().toISOString()
      }
    ];
  }

  saveUsers() {
    localStorage.setItem('mock_users', JSON.stringify(this.users));
  }

  generateId() {
    return 'USER-' + Date.now().toString().slice(-6);
  }

  hashPassword(password) {
    // Simple hash for demo purposes - in production use bcrypt
    return btoa(password + 'salt');
  }

  verifyPassword(password, hash) {
    return this.hashPassword(password) === hash;
  }

  generateToken(user) {
    // Simple token generation - in production use JWT
    return btoa(JSON.stringify({
      userId: user.id,
      email: user.email,
      role: user.role,
      exp: Date.now() + (24 * 60 * 60 * 1000) // 24 hours
    }));
  }

  verifyToken(token) {
    try {
      const payload = JSON.parse(atob(token));
      if (payload.exp < Date.now()) {
        return null; // Token expired
      }
      return payload;
    } catch (e) {
      return null;
    }
  }

  // Mock API methods
  async register(userData) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        try {
          // Check if user already exists
          const existingUser = this.users.find(u => u.email === userData.email);
          if (existingUser) {
            reject({
              response: {
                status: 400,
                data: { message: 'An account with this email already exists' }
              }
            });
            return;
          }

          // Create new user
          const newUser = {
            id: this.generateId(),
            email: userData.email,
            password: this.hashPassword(userData.password),
            first_name: userData.first_name,
            last_name: userData.last_name,
            phone: userData.phone,
            role: 'customer',
            status: 'active',
            points: 100, // Welcome bonus
            vouchers: [
              {
                id: 1,
                title: 'Welcome Bonus',
                subtitle: 'New Member Special',
                discount: '25% OFF',
                code: 'WELCOME25',
                qrCode: 'WELCOME25-QR-' + Date.now()
              }
            ],
            date_created: new Date().toISOString()
          };

          this.users.push(newUser);
          this.saveUsers();

          // Generate token
          const token = this.generateToken(newUser);

          resolve({
            data: {
              message: 'Registration successful',
              user: {
                id: newUser.id,
                email: newUser.email,
                first_name: newUser.first_name,
                last_name: newUser.last_name,
                phone: newUser.phone,
                role: newUser.role,
                points: newUser.points,
                vouchers: newUser.vouchers
              },
              access_token: token,
              token_type: 'bearer'
            }
          });
        } catch (error) {
          reject({
            response: {
              status: 400,
              data: { message: 'Registration failed' }
            }
          });
        }
      }, 1000); // Simulate network delay
    });
  }

  async login(credentials) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        try {
          const user = this.users.find(u => u.email === credentials.email);
          
          if (!user || !this.verifyPassword(credentials.password, user.password)) {
            reject({
              response: {
                status: 401,
                data: { message: 'Invalid email or password' }
              }
            });
            return;
          }

          if (user.status !== 'active') {
            reject({
              response: {
                status: 401,
                data: { message: 'Account is not active' }
              }
            });
            return;
          }

          // Generate token
          const token = this.generateToken(user);

          resolve({
            data: {
              user: {
                id: user.id,
                email: user.email,
                first_name: user.first_name,
                last_name: user.last_name,
                phone: user.phone,
                role: user.role,
                points: user.points,
                vouchers: user.vouchers
              },
              access_token: token,
              token_type: 'bearer'
            }
          });
        } catch (error) {
          reject({
            response: {
              status: 500,
              data: { message: 'Login failed' }
            }
          });
        }
      }, 1000); // Simulate network delay
    });
  }

  async getCurrentUser(token) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        try {
          const payload = this.verifyToken(token);
          if (!payload) {
            reject({
              response: {
                status: 401,
                data: { message: 'Invalid token' }
              }
            });
            return;
          }

          const user = this.users.find(u => u.id === payload.userId);
          if (!user) {
            reject({
              response: {
                status: 404,
                data: { message: 'User not found' }
              }
            });
            return;
          }

          resolve({
            data: {
              user: {
                id: user.id,
                email: user.email,
                first_name: user.first_name,
                last_name: user.last_name,
                phone: user.phone,
                role: user.role,
                points: user.points,
                vouchers: user.vouchers
              }
            }
          });
        } catch (error) {
          reject({
            response: {
              status: 500,
              data: { message: 'Failed to get user' }
            }
          });
        }
      }, 500);
    });
  }

  async logout() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ data: { message: 'Logged out successfully' } });
      }, 500);
    });
  }
}

export default new MockAuthService();
