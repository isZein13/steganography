-- Создание таблицы "auth_group"
CREATE TABLE auth_group (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) UNIQUE
);

-- Создание таблицы "auth_group_permissions"
CREATE TABLE auth_group_permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT,
    permission_id INT,
    FOREIGN KEY (group_id) REFERENCES auth_group(id),
    FOREIGN KEY (permission_id) REFERENCES auth_permission(id),
    UNIQUE KEY group_permission_unique (group_id, permission_id)
);

-- Создание таблицы "auth_permission"
CREATE TABLE auth_permission (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content_type_id INT,
    codename VARCHAR(100),
    name VARCHAR(255),
    FOREIGN KEY (content_type_id) REFERENCES django_content_type(id),
    UNIQUE KEY content_type_codename_unique (content_type_id, codename)
);

-- Создание таблицы "auth_user"
CREATE TABLE auth_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(128),
    last_login DATETIME,
    is_superuser BOOLEAN,
    username VARCHAR(150) UNIQUE,
    last_name VARCHAR(150),
    email VARCHAR(254),
    is_staff BOOLEAN,
    is_active BOOLEAN,
    date_joined DATETIME,
    first_name VARCHAR(150)
);

-- Создание таблицы "auth_user_groups"
CREATE TABLE auth_user_groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    group_id INT,
    FOREIGN KEY (user_id) REFERENCES auth_user(id),
    FOREIGN KEY (group_id) REFERENCES auth_group(id),
    UNIQUE KEY user_group_unique (user_id, group_id)
);

-- Создание таблицы "auth_user_user_permissions"
CREATE TABLE auth_user_user_permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    permission_id INT,
    FOREIGN KEY (user_id) REFERENCES auth_user(id),
    FOREIGN KEY (permission_id) REFERENCES auth_permission(id),
    UNIQUE KEY user_permission_unique (user_id, permission_id)
);

-- Создание таблицы "django_admin_log"
CREATE TABLE django_admin_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    action_time DATETIME,
    object_id TEXT,
    object_repr VARCHAR(200),
    change_message TEXT,
    content_type_id INT,
    user_id INT,
    action_flag SMALLINT,
    FOREIGN KEY (content_type_id) REFERENCES django_content_type(id),
    FOREIGN KEY (user_id) REFERENCES auth_user(id)
);

-- Создание таблицы "django_content_type"
CREATE TABLE django_content_type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    app_label VARCHAR(100),
    model VARCHAR(100),
    UNIQUE KEY app_label_model_unique (app_label, model)
);

-- Создание таблицы "django_migrations"
CREATE TABLE django_migrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    app VARCHAR(255),
    name VARCHAR(255),
    applied DATETIME
);

-- Создание таблицы "django_session"
CREATE TABLE django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT,
    expire_date DATETIME
);

-- Создание таблицы "main_photo"
CREATE TABLE main_photo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image VARCHAR(100),
    user_id INT,
    result TEXT,
    FOREIGN KEY (user_id) REFERENCES auth_user(id)
);

-- Создание таблицы "main_task"
CREATE TABLE main_task (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50),
    task TEXT
);