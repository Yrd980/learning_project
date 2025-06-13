package com.ruoyi.hotel.service;

import java.util.List;
import com.ruoyi.hotel.domain.Starhotels;

/**
 * 星级酒店信息Service接口
 * 
 * @author ningf
 * @date 2024-07-11
 */
public interface IStarhotelsService 
{
    /**
     * 查询星级酒店信息
     * 
     * @param id 星级酒店信息主键
     * @return 星级酒店信息
     */
    public Starhotels selectStarhotelsById(Long id);

    /**
     * 查询星级酒店信息列表
     * 
     * @param starhotels 星级酒店信息
     * @return 星级酒店信息集合
     */
    public List<Starhotels> selectStarhotelsList(Starhotels starhotels);

    /**
     * 新增星级酒店信息
     * 
     * @param starhotels 星级酒店信息
     * @return 结果
     */
    public int insertStarhotels(Starhotels starhotels);

    /**
     * 修改星级酒店信息
     * 
     * @param starhotels 星级酒店信息
     * @return 结果
     */
    public int updateStarhotels(Starhotels starhotels);

    /**
     * 批量删除星级酒店信息
     * 
     * @param ids 需要删除的星级酒店信息主键集合
     * @return 结果
     */
    public int deleteStarhotelsByIds(Long[] ids);

    /**
     * 删除星级酒店信息信息
     * 
     * @param id 星级酒店信息主键
     * @return 结果
     */
    public int deleteStarhotelsById(Long id);
}
