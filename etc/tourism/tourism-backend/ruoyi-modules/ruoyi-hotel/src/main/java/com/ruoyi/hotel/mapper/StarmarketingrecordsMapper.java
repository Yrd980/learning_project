package com.ruoyi.hotel.mapper;

import java.util.List;
import com.ruoyi.hotel.domain.Starmarketingrecords;

/**
 * 酒店营销记录Mapper接口
 * 
 * @author ningf
 * @date 2024-07-10
 */
public interface StarmarketingrecordsMapper 
{
    /**
     * 查询酒店营销记录
     * 
     * @param id 酒店营销记录主键
     * @return 酒店营销记录
     */
    public Starmarketingrecords selectStarmarketingrecordsById(Long id);

    /**
     * 查询酒店营销记录列表
     * 
     * @param starmarketingrecords 酒店营销记录
     * @return 酒店营销记录集合
     */
    public List<Starmarketingrecords> selectStarmarketingrecordsList(Starmarketingrecords starmarketingrecords);

    /**
     * 新增酒店营销记录
     * 
     * @param starmarketingrecords 酒店营销记录
     * @return 结果
     */
    public int insertStarmarketingrecords(Starmarketingrecords starmarketingrecords);

    /**
     * 修改酒店营销记录
     * 
     * @param starmarketingrecords 酒店营销记录
     * @return 结果
     */
    public int updateStarmarketingrecords(Starmarketingrecords starmarketingrecords);

    /**
     * 删除酒店营销记录
     * 
     * @param id 酒店营销记录主键
     * @return 结果
     */
    public int deleteStarmarketingrecordsById(Long id);

    /**
     * 批量删除酒店营销记录
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteStarmarketingrecordsByIds(Long[] ids);
}
