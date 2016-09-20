use weapp;
update account_user_profile set webapp_type = 2 where user_id = (select id from auth_user where username = 'guo');
update account_user_profile set store_name = (select username from auth_user where id = account_user_profile.user_id);