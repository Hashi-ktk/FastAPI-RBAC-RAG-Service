# Admins can manage all resources
allow("admin", "manage", "all");

# Admins can perform CRUD operations on users
allow("admin", "create", "user");
allow("admin", "read", "user");
allow("admin", "update", "user");
allow("admin", "delete", "user");
allow("admin", "list", "users");

# Users can only view or update their own information
allow("user", "view", "self") if
    _resource.id = _actor.id;

allow("user", "update", "self") if
    _resource.id = _actor.id;