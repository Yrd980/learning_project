package com.ruoyi.guestHotel.service;

import java.util.List;
import com.ruoyi.guestHotel.domain.Nonstarhotels;

/**
 * 非星级酒店Service接口
 * 
 * @author ruoyi
 * @date 2024-07-11
 */
public interface INonstarhotelsService 
{
    /**
     * 查询非星级酒店
     * 
     * @param id 非星级酒店主键
     * @return 非星级酒店
     */
    public Nonstarhotels selectNonstarhotelsById(Long id);

    /**
     * 查询非星级酒店列表
     * 
     * @param nonstarhotels 非星级酒店
     * @return 非星级酒店集合
     */
    public List<Nonstarhotels> selectNonstarhotelsList(Nonstarhotels nonstarhotels);

}
