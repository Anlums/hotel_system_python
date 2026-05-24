-- ============================================================
-- 天玺尊邸酒店管理系统 - 数据库初始化脚本
-- MySQL 8.0 + InnoDB + utf8mb4
-- ============================================================

-- 创建数据库（如果 docker-compose 已自动创建则跳过）
CREATE DATABASE IF NOT EXISTS hotel_system
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE hotel_system;

-- ==================== 1. 房间表 ====================
CREATE TABLE IF NOT EXISTS rooms (
    id          BIGINT       NOT NULL AUTO_INCREMENT COMMENT '房间ID',
    room_number BIGINT       NOT NULL                COMMENT '房间编号',
    type        VARCHAR(50)  NOT NULL                COMMENT '房型',
    price       DECIMAL(10,2) NOT NULL               COMMENT '每晚价格',
    status      SMALLINT     DEFAULT 0               COMMENT '状态: 0-空闲, 1-已预订, 2-已入住, 3-清洁中',
    create_time DATETIME     DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (id),
    UNIQUE KEY uk_room_number (room_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='房间';

-- ==================== 2. 预订/订单表 ====================
CREATE TABLE IF NOT EXISTS bookings (
    id             BIGINT        NOT NULL AUTO_INCREMENT COMMENT '预订ID',
    room_number    BIGINT        NOT NULL                COMMENT '房间编号',
    guest_name     VARCHAR(50)   NOT NULL                COMMENT '入住人姓名',
    phone          VARCHAR(20)   NOT NULL                COMMENT '联系电话',
    check_in_date  DATETIME      NOT NULL                COMMENT '入住日期',
    check_out_date DATETIME      NOT NULL                COMMENT '退房日期',
    total_amount   DECIMAL(10,2) NOT NULL                COMMENT '订单总金额',
    status         SMALLINT      DEFAULT 1               COMMENT '订单状态: 1-已预约, 2-已入住, 3-已退房, 4-已取消',
    create_time    DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (id),
    INDEX idx_room_number (room_number),
    INDEX idx_guest_name (guest_name),
    INDEX idx_status (status),
    INDEX idx_check_in (check_in_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='预订';

-- ==================== 3. 清洁任务表 ====================
CREATE TABLE IF NOT EXISTS cleaning_tasks (
    id           BIGINT       NOT NULL AUTO_INCREMENT COMMENT '工单ID',
    room_number  BIGINT       NOT NULL                COMMENT '房间号',
    booking_id   BIGINT                               COMMENT '关联订单ID',
    status       SMALLINT     DEFAULT 0               COMMENT '状态: 0-待清洁, 1-清洁中, 2-已完成',
    assignee     VARCHAR(50)                          COMMENT '保洁人员',
    created_at   DATETIME     DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    completed_at DATETIME                             COMMENT '完成时间',
    remark       VARCHAR(500)                         COMMENT '备注',
    PRIMARY KEY (id),
    INDEX idx_room_number (room_number),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='清洁任务';

-- ==================== 4. 服务菜单表 ====================
CREATE TABLE IF NOT EXISTS service_menu (
    id         BIGINT        NOT NULL AUTO_INCREMENT COMMENT 'ID',
    name       VARCHAR(100)  NOT NULL                COMMENT '项目名称',
    category   VARCHAR(50)   NOT NULL                COMMENT '分类: 餐饮/日用品/其他',
    price      DECIMAL(10,2) NOT NULL DEFAULT 0      COMMENT '价格',
    available  SMALLINT      DEFAULT 1               COMMENT '是否可用: 1-是, 0-否',
    created_at DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (id),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='服务菜单项';

-- ==================== 5. 客房服务订单表 ====================
CREATE TABLE IF NOT EXISTS room_service_orders (
    id           BIGINT        NOT NULL AUTO_INCREMENT COMMENT '订单ID',
    room_number  BIGINT        NOT NULL                COMMENT '房间号',
    guest_name   VARCHAR(50)                           COMMENT '客人姓名',
    items        TEXT          NOT NULL                COMMENT '订单项目(JSON数组)',
    total_amount DECIMAL(10,2) NOT NULL DEFAULT 0      COMMENT '总金额',
    status       SMALLINT      DEFAULT 0               COMMENT '状态: 0-待处理, 1-配送中, 2-已完成, 3-已取消',
    remark       VARCHAR(500)                          COMMENT '备注',
    created_at   DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    completed_at DATETIME                              COMMENT '完成时间',
    PRIMARY KEY (id),
    INDEX idx_room_number (room_number),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='客房服务订单';

-- ==================== 6. 调价历史表 ====================
CREATE TABLE IF NOT EXISTS price_history (
    id         BIGINT        NOT NULL AUTO_INCREMENT COMMENT '记录ID',
    room_type  VARCHAR(50)   NOT NULL                COMMENT '房型',
    old_price  DECIMAL(10,2) NOT NULL                COMMENT '原价',
    new_price  DECIMAL(10,2) NOT NULL                COMMENT '新价',
    reason     VARCHAR(500)                          COMMENT '调价原因(AI分析)',
    created_at DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '调价时间',
    PRIMARY KEY (id),
    INDEX idx_room_type (room_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='调价历史';

-- ==================== 7. 会员表 ====================
CREATE TABLE IF NOT EXISTS members (
    id          BIGINT         NOT NULL AUTO_INCREMENT COMMENT '会员ID',
    name        VARCHAR(50)    NOT NULL                COMMENT '姓名',
    phone       VARCHAR(20)    NOT NULL                COMMENT '手机号',
    id_card     VARCHAR(18)                            COMMENT '身份证号',
    email       VARCHAR(100)                           COMMENT '邮箱',
    level       SMALLINT       DEFAULT 0               COMMENT '等级: 0-普通, 1-银卡, 2-金卡, 3-钻石',
    points      BIGINT         DEFAULT 0               COMMENT '积分',
    total_spent DECIMAL(12,2)  DEFAULT 0               COMMENT '累计消费',
    created_at  DATETIME       DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    updated_at  DATETIME       DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (id),
    UNIQUE KEY uk_phone (phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员';

-- ==================== 8. 支付记录表 ====================
CREATE TABLE IF NOT EXISTS payments (
    id         BIGINT        NOT NULL AUTO_INCREMENT COMMENT '支付ID',
    booking_id BIGINT        NOT NULL                COMMENT '关联订单ID',
    type       VARCHAR(20)   NOT NULL                COMMENT '类型: deposit=押金, payment=房费, refund=退款',
    amount     DECIMAL(10,2) NOT NULL                COMMENT '金额(正数=收入, 负数=支出)',
    method     VARCHAR(20)   DEFAULT 'cash'           COMMENT '支付方式: cash/wechat/alipay/card',
    status     VARCHAR(20)   DEFAULT 'completed'      COMMENT '状态: completed/refunded',
    remark     TEXT                                   COMMENT '备注',
    operator   VARCHAR(50)   DEFAULT '系统'            COMMENT '操作人',
    created_at DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (id),
    INDEX idx_booking_id (booking_id),
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='支付';

-- ==================== 示例数据（房间） ====================
INSERT IGNORE INTO rooms (room_number, type, price, status) VALUES
-- 标准间
(101, '标准间', 299.00, 0),
(102, '标准间', 299.00, 0),
(103, '标准间', 299.00, 0),
(104, '标准间', 299.00, 0),
(105, '标准间', 299.00, 0),
-- 大床房
(106, '大床房', 499.00, 0),
(107, '大床房', 499.00, 0),
(108, '大床房', 499.00, 0),
-- 双床房
(109, '双床房', 499.00, 0),
(110, '双床房', 499.00, 0),
-- 商务套房
(111, '商务套房', 899.00, 0),
(112, '商务套房', 899.00, 0),
-- 豪华套房
(113, '豪华套房', 1599.00, 0),
-- 总统套房
(114, '总统套房', 2999.00, 0),
-- 亲子房
(115, '亲子房', 699.00, 0),
(116, '亲子房', 699.00, 0),
-- 爱情房间
(117, '爱情房间', 599.00, 0),
-- 小床房
(118, '小床房', 199.00, 0);
