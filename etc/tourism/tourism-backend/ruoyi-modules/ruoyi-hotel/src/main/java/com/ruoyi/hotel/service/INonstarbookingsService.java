package com.ruoyi.hotel.service;

import java.util.List;
import com.ruoyi.hotel.domain.Nonstarbookings;

/**
 * 非星级酒店预定信息Service接口
 * 
 * @author ningf
 * @date 2024-07-14
 */
public interface INonstarbookingsService {
    /**
     * 查询非星级酒店预定信息
     *
     * @param id 非星级酒店预定信息主键
     * @return 非星级酒店预定信息
     */
    public Nonstarbookings selectNonstarbookingsById(Long id);

    /**
     * 查询非星级酒店预定信息列表
     *
     * @param nonstarbookings 非星级酒店预定信息
     * @return 非星级酒店预定信息集合
     */
    public List<Nonstarbookings> selectNonstarbookingsList(Nonstarbookings nonstarbookings);

    /**
     * 新增非星级酒店预定信息
     *
     * @param nonstarbookings 非星级酒店预定信息
     * @return 结果
     */
    public int insertNonstarbookings(Nonstarbookings nonstarbookings);

    /**
     * 修改非星级酒店预定信息
     *
     * @param nonstarbookings 非星级酒店预定信息
     * @return 结果
     */
    public int updateNonstarbookings(Nonstarbookings nonstarbookings);

    /**
     * 批量删除非星级酒店预定信息
     *
     * @param ids 需要删除的非星级酒店预定信息主键集合
     * @return 结果
     */
    public int deleteNonstarbookingsByIds(Long[] ids);

    /**
     * 删除非星级酒店预定信息信息
     *
     * @param id 非星级酒店预定信息主键
     * @return 结果
     */
    public int deleteNonstarbookingsById(Long id);

    public int confirmNonstarbookingsByIds(Long[] ids);
}
