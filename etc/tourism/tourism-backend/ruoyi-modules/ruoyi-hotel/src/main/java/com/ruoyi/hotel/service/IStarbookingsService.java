package com.ruoyi.hotel.service;

import java.util.List;
import com.ruoyi.hotel.domain.Starbookings;

/**
 * 星级酒店预定信息Service接口
 * 
 * @author ningf
 * @date 2024-07-11
 */
public interface IStarbookingsService 
{
    /**
     * 查询星级酒店预定信息
     * 
     * @param id 星级酒店预定信息主键
     * @return 星级酒店预定信息
     */
    public Starbookings selectStarbookingsById(Long id);

    /**
     * 查询星级酒店预定信息列表
     * 
     * @param starbookings 星级酒店预定信息
     * @return 星级酒店预定信息集合
     */
    public List<Starbookings> selectStarbookingsList(Starbookings starbookings);

    /**
     * 新增星级酒店预定信息
     * 
     * @param starbookings 星级酒店预定信息
     * @return 结果
     */
    public int insertStarbookings(Starbookings starbookings);

    /**
     * 修改星级酒店预定信息
     * 
     * @param starbookings 星级酒店预定信息
     * @return 结果
     */
    public int updateStarbookings(Starbookings starbookings);

    /**
     * 批量删除星级酒店预定信息
     * 
     * @param ids 需要删除的星级酒店预定信息主键集合
     * @return 结果
     */
    public int deleteStarbookingsByIds(Long[] ids);

    /**
     * 删除星级酒店预定信息信息
     * 
     * @param id 星级酒店预定信息主键
     * @return 结果
     */
    public int deleteStarbookingsById(Long id);

    public int confirmStarbookingsByIds(Long[] ids);
}
