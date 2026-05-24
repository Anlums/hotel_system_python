-- 天玺尊邸酒店管理系统 - 完整数据导出

TRUNCATE TABLE `rooms`;
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (1, 101, '爱情房间', '416.00', 1, '2026-04-28 08:14:04', '2026-05-22 09:16:31');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (2, 102, '小床房', '180.00', 1, '2026-04-28 08:14:58', '2026-05-22 09:16:30');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (3, 103, '大床房', '250.00', 0, '2026-04-28 08:15:09', '2026-05-22 10:22:37');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (4, 104, '双床房', '360.00', 3, '2026-04-28 08:15:24', '2026-05-22 09:16:29');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (5, 105, '总统套房', '720.00', 1, '2026-04-28 08:15:40', '2026-05-22 09:16:30');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (11, 106, '标准间', '200.00', 1, '2026-04-30 15:33:34', '2026-04-30 15:53:24');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (12, 107, '标准间', '200.00', 1, '2026-04-30 15:33:53', '2026-04-30 15:53:31');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (13, 108, '标准间', '200.00', 0, '2026-04-30 15:34:01', '2026-05-22 10:22:38');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (14, 109, '标准间', '200.00', 0, '2026-04-30 15:34:08', '2026-04-30 15:34:08');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (15, 110, '标准间', '200.00', 0, '2026-04-30 15:34:14', '2026-05-22 10:09:47');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (16, 111, '大床房', '300.00', 1, '2026-04-30 15:34:46', '2026-04-30 15:53:00');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (17, 112, '大床房', '300.00', 3, '2026-04-30 15:34:55', '2026-05-22 09:52:26');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (18, 113, '大床房', '300.00', 0, '2026-04-30 15:35:01', '2026-05-19 13:14:27');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (19, 114, '豪华套房', '300.00', 1, '2026-04-30 15:35:26', '2026-05-22 09:16:40');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (20, 115, '豪华套房', '300.00', 0, '2026-04-30 15:35:33', '2026-05-22 09:16:40');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (21, 116, '豪华套房', '300.00', 3, '2026-04-30 15:35:40', '2026-05-22 10:24:59');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (22, 117, '标准间', '200.00', 0, '2026-04-30 15:35:51', '2026-04-30 15:35:51');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (23, 118, '大床房', '200.00', 0, '2026-04-30 15:35:57', '2026-04-30 15:35:57');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (24, 119, '豪华套房', '300.00', 0, '2026-04-30 15:36:04', '2026-05-22 09:16:40');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (25, 120, '豪华套房', '300.00', 0, '2026-04-30 15:36:13', '2026-05-22 09:16:40');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (26, 520, '爱情房间', '416.00', 0, '2026-04-30 15:46:02', '2026-05-22 09:16:31');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (27, 521, '爱情房间', '416.00', 0, '2026-04-30 15:46:20', '2026-05-22 09:16:31');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (28, 121, '亲子房', '160.00', 0, '2026-04-30 15:47:34', '2026-05-22 09:16:18');
INSERT INTO `rooms` (`id`, `room_number`, `type`, `price`, `status`, `create_time`, `update_time`) VALUES (29, 122, '总统套房', '1000.00', 1, '2026-05-22 10:11:48', '2026-05-22 13:52:38');
-- rooms: 24 rows

TRUNCATE TABLE `bookings`;
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (1, 101, 'Anlums and Jenny', '123456789', '2026-04-26 00:00:00', '2026-04-28 10:28:34', '1040.00', 3, '2026-04-28 08:23:54');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (2, 102, 'Anlums', '123456789', '2026-05-01 00:00:00', '2026-04-28 10:28:36', '150.00', 3, '2026-04-28 08:31:26');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (3, 103, 'ccc', '123456789', '2026-04-26 00:00:00', '2026-04-28 10:28:37', '500.00', 3, '2026-04-28 08:31:33');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (5, 104, 'ddd', '123456789', '2026-04-26 00:00:00', '2026-04-28 10:44:27', '600.00', 3, '2026-04-28 09:16:52');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (6, 101, 'ddd', '123456789', '2026-04-26 14:00:00', '2026-04-28 10:28:49', '520.00', 3, '2026-04-28 10:21:46');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (7, 102, 'ddd', '123456789', '2026-04-26 14:00:00', '2026-04-29 14:28:49', '450.00', 3, '2026-04-28 10:21:52');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (8, 103, 'ddd', '123456789', '2026-04-26 14:00:00', '2026-04-29 14:39:48', '750.00', 3, '2026-04-28 10:22:33');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (9, 105, 'new', '123', '2026-04-28 10:41:49', '2026-04-28 10:44:23', '600.00', 3, '2026-04-28 10:43:54');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (10, 101, 'new', '111', '2026-04-29 14:22:41', '2026-04-29 15:31:01', '520.00', 3, '2026-04-29 14:22:42');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (11, 102, 'new', '111', '2026-04-29 14:39:44', '2000-01-01 00:00:00', '0.00', 4, '2026-04-29 14:39:45');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (12, 101, 'new', '111', '2026-04-29 15:33:09', '2026-04-29 15:40:25', '520.00', 3, '2026-04-29 15:33:09');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (13, 102, 'new', '111', '2026-04-29 15:33:21', '2026-04-29 15:40:29', '150.00', 3, '2026-04-29 15:33:22');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (14, 101, 'new', '111', '2026-04-29 15:40:47', '2000-01-01 00:00:00', '0.00', 4, '2026-04-29 15:40:48');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (15, 104, 'new111', '111aaa', '2026-04-29 16:05:49', '2026-04-29 20:33:51', '300.00', 3, '2026-04-29 15:41:06');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (16, 102, 'new', '111', '2026-04-29 15:41:12', '2000-01-01 00:00:00', '0.00', 1, '2026-04-29 15:41:13');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (17, 102, 'new', '111', '2026-04-29 16:06:02', '2000-01-01 00:00:00', '0.00', 4, '2026-04-29 16:06:02');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (18, 101, 'new', '111', '2026-04-29 16:39:22', '2000-01-01 00:00:00', '0.00', 2, '2026-04-29 16:39:30');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (19, 105, 'new', '111', '2026-04-29 19:59:34', '2000-01-01 00:00:00', '0.00', 2, '2026-04-29 19:59:34');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (20, 110, 'new', '111', '2026-04-30 15:34:28', '2026-05-22 09:53:07', '4200.00', 3, '2026-04-30 15:34:29');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (21, 111, 'new', '111', '2026-04-30 15:52:55', '2000-01-01 00:00:00', '0.00', 2, '2026-04-30 15:53:00');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (22, 112, 'new', '111', '2026-04-30 15:53:05', '2026-05-22 09:52:27', '6300.00', 3, '2026-04-30 15:53:06');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (23, 113, 'new', '111', '2026-04-30 15:53:12', '2026-05-19 13:14:18', '5400.00', 3, '2026-04-30 15:53:13');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (24, 106, 'new', '111', '2026-04-30 15:53:24', '2000-01-01 00:00:00', '0.00', 1, '2026-04-30 15:53:24');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (25, 107, 'new', '111', '2026-04-30 15:53:31', '2000-01-01 00:00:00', '0.00', 1, '2026-04-30 15:53:31');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (26, 108, 'test', '13800000000', '2026-05-19 00:00:00', '2026-05-19 13:13:29', '200.00', 3, '2026-05-19 13:13:23');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (27, 114, '李四', '13800001111', '2026-06-01 00:00:00', '2026-06-03 00:00:00', '748.00', 1, '2026-05-19 13:43:29');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (28, 103, '测试押金', '13800000002', '2026-05-18 00:00:00', '2026-05-19 14:43:04', '250.00', 3, '2026-05-19 14:42:32');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (29, 104, 'test2', '13800000003', '2026-05-18 00:00:00', '2026-05-19 14:43:31', '300.00', 3, '2026-05-19 14:43:22');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (30, 103, 'aa', '11', '2026-05-22 10:03:14', '2026-05-22 10:03:37', '250.00', 3, '2026-05-22 10:03:15');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (33, 116, 'test', '111', '2026-05-22 10:24:22', '2026-05-22 10:24:59', '300.00', 3, '2026-05-22 10:24:39');
INSERT INTO `bookings` (`id`, `room_number`, `guest_name`, `phone`, `check_in_date`, `check_out_date`, `total_amount`, `status`, `create_time`) VALUES (34, 122, 'test', '11', '2026-05-22 13:51:58', '2026-05-23 12:00:00', '1000.00', 1, '2026-05-22 13:52:38');
-- bookings: 31 rows

TRUNCATE TABLE `cleaning_tasks`;
INSERT INTO `cleaning_tasks` (`id`, `room_number`, `booking_id`, `status`, `assignee`, `created_at`, `completed_at`, `remark`) VALUES (1, 108, 26, 2, '张姐', '2026-05-19 13:13:28', '2026-05-19 13:13:39', NULL);
INSERT INTO `cleaning_tasks` (`id`, `room_number`, `booking_id`, `status`, `assignee`, `created_at`, `completed_at`, `remark`) VALUES (2, 113, 23, 2, 'aaa', '2026-05-19 13:14:18', '2026-05-19 13:14:27', NULL);
INSERT INTO `cleaning_tasks` (`id`, `room_number`, `booking_id`, `status`, `assignee`, `created_at`, `completed_at`, `remark`) VALUES (3, 103, 28, 2, 'a', '2026-05-19 14:43:04', '2026-05-22 10:09:43', NULL);
INSERT INTO `cleaning_tasks` (`id`, `room_number`, `booking_id`, `status`, `assignee`, `created_at`, `completed_at`, `remark`) VALUES (4, 104, 29, 0, NULL, '2026-05-19 14:43:30', NULL, NULL);
INSERT INTO `cleaning_tasks` (`id`, `room_number`, `booking_id`, `status`, `assignee`, `created_at`, `completed_at`, `remark`) VALUES (5, 112, 22, 0, NULL, '2026-05-22 09:52:26', NULL, NULL);
INSERT INTO `cleaning_tasks` (`id`, `room_number`, `booking_id`, `status`, `assignee`, `created_at`, `completed_at`, `remark`) VALUES (6, 110, 20, 2, 'a', '2026-05-22 09:53:07', '2026-05-22 10:09:47', NULL);
INSERT INTO `cleaning_tasks` (`id`, `room_number`, `booking_id`, `status`, `assignee`, `created_at`, `completed_at`, `remark`) VALUES (7, 103, 30, 0, NULL, '2026-05-22 10:03:37', NULL, NULL);
INSERT INTO `cleaning_tasks` (`id`, `room_number`, `booking_id`, `status`, `assignee`, `created_at`, `completed_at`, `remark`) VALUES (8, 116, 33, 0, NULL, '2026-05-22 10:24:59', NULL, NULL);
-- cleaning_tasks: 8 rows

TRUNCATE TABLE `service_menu`;
INSERT INTO `service_menu` (`id`, `name`, `category`, `price`, `available`, `created_at`) VALUES (1, '牛肉面', '餐饮', '28.00', 1, '2026-05-19 13:20:32');
INSERT INTO `service_menu` (`id`, `name`, `category`, `price`, `available`, `created_at`) VALUES (2, '咖啡', '饮品', '18.00', 1, '2026-05-19 13:20:40');
INSERT INTO `service_menu` (`id`, `name`, `category`, `price`, `available`, `created_at`) VALUES (3, '毛巾套装', '日用品', '15.00', 1, '2026-05-19 13:20:40');
INSERT INTO `service_menu` (`id`, `name`, `category`, `price`, `available`, `created_at`) VALUES (4, '矿泉水', '饮品', '2.00', 1, '2026-05-22 10:09:59');
-- service_menu: 4 rows

TRUNCATE TABLE `room_service_orders`;
INSERT INTO `room_service_orders` (`id`, `room_number`, `guest_name`, `items`, `total_amount`, `status`, `remark`, `created_at`, `completed_at`) VALUES (1, 108, '测试客人', '[{"name": "\\u725b\\u8089\\u9762", "price": 28, "qty": 2}]', '56.00', 2, NULL, '2026-05-19 13:20:52', '2026-05-19 13:20:53');
INSERT INTO `room_service_orders` (`id`, `room_number`, `guest_name`, `items`, `total_amount`, `status`, `remark`, `created_at`, `completed_at`) VALUES (2, 109, '张三', '[{"name": "\\u5496\\u5561", "price": 18, "qty": 2}]', '36.00', 2, NULL, '2026-05-19 13:21:23', '2026-05-19 13:21:24');
INSERT INTO `room_service_orders` (`id`, `room_number`, `guest_name`, `items`, `total_amount`, `status`, `remark`, `created_at`, `completed_at`) VALUES (3, 112, 'anlums', '[{"name":"毛巾套装","price":15,"qty":4},{"name":"牛肉面","price":28,"qty":4},{"name":"咖啡","price":18,"qty":1}]', '190.00', 2, NULL, '2026-05-22 09:11:43', '2026-05-22 09:13:07');
INSERT INTO `room_service_orders` (`id`, `room_number`, `guest_name`, `items`, `total_amount`, `status`, `remark`, `created_at`, `completed_at`) VALUES (4, 112, 'anlums', '[{"name":"毛巾套装","price":15,"qty":1}]', '15.00', 1, NULL, '2026-05-22 09:12:42', NULL);
INSERT INTO `room_service_orders` (`id`, `room_number`, `guest_name`, `items`, `total_amount`, `status`, `remark`, `created_at`, `completed_at`) VALUES (5, 101, NULL, '[{"name":"矿泉水","price":2,"qty":1}]', '2.00', 0, NULL, '2026-05-22 10:10:10', NULL);
-- room_service_orders: 5 rows

TRUNCATE TABLE `price_history`;
INSERT INTO `price_history` (`id`, `room_type`, `old_price`, `new_price`, `reason`, `created_at`) VALUES (1, '豪华套房', '500.00', '374.00', '闲置率高，降价15%提升竞争力', '2026-05-19 13:35:40');
INSERT INTO `price_history` (`id`, `room_type`, `old_price`, `new_price`, `reason`, `created_at`) VALUES (2, '亲子房', '200.00', '160.00', '入住率0%，降价20%吸引预订', '2026-05-22 09:16:18');
INSERT INTO `price_history` (`id`, `room_type`, `old_price`, `new_price`, `reason`, `created_at`) VALUES (3, '亲子房', '160.00', '160.00', '入住率0%，降价20%吸引预订', '2026-05-22 09:16:19');
INSERT INTO `price_history` (`id`, `room_type`, `old_price`, `new_price`, `reason`, `created_at`) VALUES (4, '亲子房', '160.00', '160.00', '入住率0%，降价20%吸引预订', '2026-05-22 09:16:20');
INSERT INTO `price_history` (`id`, `room_type`, `old_price`, `new_price`, `reason`, `created_at`) VALUES (5, '亲子房', '160.00', '160.00', '入住率0%，降价20%吸引预订', '2026-05-22 09:16:21');
INSERT INTO `price_history` (`id`, `room_type`, `old_price`, `new_price`, `reason`, `created_at`) VALUES (6, '亲子房', '160.00', '160.00', '入住率0%，降价20%吸引预订', '2026-05-22 09:16:21');
INSERT INTO `price_history` (`id`, `room_type`, `old_price`, `new_price`, `reason`, `created_at`) VALUES (7, '双床房', '300.00', '360.00', '入住率100%，涨价20%提升收益', '2026-05-22 09:16:29');
INSERT INTO `price_history` (`id`, `room_type`, `old_price`, `new_price`, `reason`, `created_at`) VALUES (8, '小床房', '150.00', '180.00', '入住率100%，涨价20%', '2026-05-22 09:16:30');
INSERT INTO `price_history` (`id`, `room_type`, `old_price`, `new_price`, `reason`, `created_at`) VALUES (9, '总统套房', '600.00', '720.00', '入住率100%，涨价20%', '2026-05-22 09:16:30');
INSERT INTO `price_history` (`id`, `room_type`, `old_price`, `new_price`, `reason`, `created_at`) VALUES (10, '爱情房间', '520.00', '416.00', '入住率33.3%，降价20%', '2026-05-22 09:16:31');
INSERT INTO `price_history` (`id`, `room_type`, `old_price`, `new_price`, `reason`, `created_at`) VALUES (11, '豪华套房', '374.00', '300.00', '入住率20%，降价20%', '2026-05-22 09:16:40');
-- price_history: 11 rows

TRUNCATE TABLE `members`;
INSERT INTO `members` (`id`, `name`, `phone`, `id_card`, `email`, `level`, `points`, `total_spent`, `created_at`, `updated_at`) VALUES (1, '王五', '13900001111', '110101199001011234', NULL, 1, 2200, '0.00', '2026-05-19 13:51:59', '2026-05-19 14:50:00');
INSERT INTO `members` (`id`, `name`, `phone`, `id_card`, `email`, `level`, `points`, `total_spent`, `created_at`, `updated_at`) VALUES (2, '赵六', '13900002222', NULL, 'zhao6@test.com', 0, 0, '0.00', '2026-05-19 13:51:59', '2026-05-19 13:51:59');
INSERT INTO `members` (`id`, `name`, `phone`, `id_card`, `email`, `level`, `points`, `total_spent`, `created_at`, `updated_at`) VALUES (3, 'anlums', '123', 'asd', 'asd', 0, 300, '0.00', '2026-05-22 09:49:56', '2026-05-22 09:50:17');
-- members: 3 rows

TRUNCATE TABLE `payments`;
INSERT INTO `payments` (`id`, `booking_id`, `type`, `amount`, `method`, `status`, `remark`, `operator`, `created_at`, `updated_at`) VALUES (1, 28, 'deposit', '500.00', 'wechat', 'completed', '入住押金', '前台', '2026-05-19 14:42:34', '2026-05-19 14:42:34');
INSERT INTO `payments` (`id`, `booking_id`, `type`, `amount`, `method`, `status`, `remark`, `operator`, `created_at`, `updated_at`) VALUES (2, 28, 'refund', '-250.00', 'wechat', 'completed', '退房退款（押金500.0 - 房费250.00）', 'qiantai', '2026-05-19 14:43:02', '2026-05-19 14:43:02');
INSERT INTO `payments` (`id`, `booking_id`, `type`, `amount`, `method`, `status`, `remark`, `operator`, `created_at`, `updated_at`) VALUES (3, 29, 'deposit', '200.00', 'cash', 'completed', '入住押金', 'qiantai', '2026-05-19 14:43:24', '2026-05-19 14:43:24');
INSERT INTO `payments` (`id`, `booking_id`, `type`, `amount`, `method`, `status`, `remark`, `operator`, `created_at`, `updated_at`) VALUES (4, 29, 'payment', '100.00', 'alipay', 'completed', '退房补交房费（总300.00 - 押金200.0）', 'qiantai', '2026-05-19 14:43:28', '2026-05-19 14:43:28');
INSERT INTO `payments` (`id`, `booking_id`, `type`, `amount`, `method`, `status`, `remark`, `operator`, `created_at`, `updated_at`) VALUES (5, 22, 'payment', '6300.00', 'wechat', 'completed', '退房补交房费（总6300.00 - 押金0.0）', '前台', '2026-05-22 09:52:26', '2026-05-22 09:52:26');
INSERT INTO `payments` (`id`, `booking_id`, `type`, `amount`, `method`, `status`, `remark`, `operator`, `created_at`, `updated_at`) VALUES (6, 21, 'deposit', '500.00', 'alipay', 'completed', '入住押金', '前台', '2026-05-22 09:52:42', '2026-05-22 09:52:42');
INSERT INTO `payments` (`id`, `booking_id`, `type`, `amount`, `method`, `status`, `remark`, `operator`, `created_at`, `updated_at`) VALUES (7, 19, 'deposit', '500.00', 'cash', 'completed', '入住押金', '前台', '2026-05-22 09:52:51', '2026-05-22 09:52:51');
INSERT INTO `payments` (`id`, `booking_id`, `type`, `amount`, `method`, `status`, `remark`, `operator`, `created_at`, `updated_at`) VALUES (8, 20, 'payment', '4200.00', 'wechat', 'completed', '退房补交房费（总4200.00 - 押金0.0）', '前台', '2026-05-22 09:53:06', '2026-05-22 09:53:06');
INSERT INTO `payments` (`id`, `booking_id`, `type`, `amount`, `method`, `status`, `remark`, `operator`, `created_at`, `updated_at`) VALUES (9, 30, 'deposit', '500.00', 'cash', 'completed', '入住押金', '前台', '2026-05-22 10:03:30', '2026-05-22 10:03:30');
INSERT INTO `payments` (`id`, `booking_id`, `type`, `amount`, `method`, `status`, `remark`, `operator`, `created_at`, `updated_at`) VALUES (10, 30, 'refund', '-250.00', 'cash', 'completed', '退房退款（押金500.0 - 房费250.00）', '前台', '2026-05-22 10:03:37', '2026-05-22 10:03:37');
INSERT INTO `payments` (`id`, `booking_id`, `type`, `amount`, `method`, `status`, `remark`, `operator`, `created_at`, `updated_at`) VALUES (11, 33, 'deposit', '500.00', 'cash', 'completed', '入住押金', '前台', '2026-05-22 10:24:53', '2026-05-22 10:24:53');
INSERT INTO `payments` (`id`, `booking_id`, `type`, `amount`, `method`, `status`, `remark`, `operator`, `created_at`, `updated_at`) VALUES (12, 33, 'refund', '-200.00', 'cash', 'completed', '退房退款（押金500.0 - 房费300.00）', '前台', '2026-05-22 10:24:59', '2026-05-22 10:24:59');
-- payments: 12 rows

