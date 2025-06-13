package com.ruoyi.hotel.mapper;

import java.util.List;
import com.ruoyi.hotel.domain.Starhotelreviews;

/**
 * 星级酒店评价Mapper接口
 * 
 * @author ningf
 * @date 2024-07-15
 */
public interface StarhotelreviewsMapper 
{
    /**
     * 查询星级酒店评价
     * 
     * @param id 星级酒店评价主键
     * @return 星级酒店评价
     */
    public Starhotelreviews selectStarhotelreviewsById(Long id);

    /**
     * 查询星级酒店评价列表
     * 
     * @param starhotelreviews 星级酒店评价
     * @return 星级酒店评价集合
     */
    public List<Starhotelreviews> selectStarhotelreviewsList(Starhotelreviews starhotelreviews);

    /**
     * 新增星级酒店评价
     * 
     * @param starhotelreviews 星级酒店评价
     * @return 结果
     */
    public int insertStarhotelreviews(Starhotelreviews starhotelreviews);

    /**
     * 修改星级酒店评价
     * 
     * @param starhotelreviews 星级酒店评价
     * @return 结果
     */
    public int updateStarhotelreviews(Starhotelreviews starhotelreviews);

    /**
     * 删除星级酒店评价
     * 
     * @param id 星级酒店评价主键
     * @return 结果
     */
    public int deleteStarhotelreviewsById(Long id);

    /**
     * 批量删除星级酒店评价
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteStarhotelreviewsByIds(Long[] ids);
}
