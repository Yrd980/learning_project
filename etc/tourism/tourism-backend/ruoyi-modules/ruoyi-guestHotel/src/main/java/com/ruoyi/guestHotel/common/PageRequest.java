package com.ruoyi.guestHotel.common;

import lombok.Data;

import java.io.Serializable;

/**
 * 通用分页请求类
 */
@Data
public class PageRequest implements Serializable {

    private static final long serialVersionUID = -3710295420279048388L;

    /**
     * 页面大小
     */
    private long size = 8;

    /**
     * 当前页面
     */
    private long current = 1;
}
