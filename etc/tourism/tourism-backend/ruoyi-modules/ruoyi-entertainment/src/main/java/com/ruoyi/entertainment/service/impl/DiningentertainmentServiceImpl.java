package com.ruoyi.entertainment.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.entertainment.mapper.DiningentertainmentMapper;
import com.ruoyi.entertainment.domain.Diningentertainment;
import com.ruoyi.entertainment.service.IDiningentertainmentService;

/**
 * 餐饮娱乐信息Service业务层处理
 * 
 * @author ningf
 * @date 2024-07-08
 */
@Service
public class DiningentertainmentServiceImpl implements IDiningentertainmentService 
{
    @Autowired
    private DiningentertainmentMapper diningentertainmentMapper;

    /**
     * 查询餐饮娱乐信息
     * 
     * @param id 餐饮娱乐信息主键
     * @return 餐饮娱乐信息
     */
    @Override
    public Diningentertainment selectDiningentertainmentById(Long id)
    {
        return diningentertainmentMapper.selectDiningentertainmentById(id);
    }

    /**
     * 查询餐饮娱乐信息列表
     * 
     * @param diningentertainment 餐饮娱乐信息
     * @return 餐饮娱乐信息
     */
    @Override
    public List<Diningentertainment> selectDiningentertainmentList(Diningentertainment diningentertainment)
    {
        return diningentertainmentMapper.selectDiningentertainmentList(diningentertainment);
    }

    /**
     * 新增餐饮娱乐信息
     * 
     * @param diningentertainment 餐饮娱乐信息
     * @return 结果
     */
    @Override
    public int insertDiningentertainment(Diningentertainment diningentertainment)
    {
        return diningentertainmentMapper.insertDiningentertainment(diningentertainment);
    }

    /**
     * 修改餐饮娱乐信息
     * 
     * @param diningentertainment 餐饮娱乐信息
     * @return 结果
     */
    @Override
    public int updateDiningentertainment(Diningentertainment diningentertainment)
    {
        return diningentertainmentMapper.updateDiningentertainment(diningentertainment);
    }

    /**
     * 批量删除餐饮娱乐信息
     * 
     * @param ids 需要删除的餐饮娱乐信息主键
     * @return 结果
     */
    @Override
    public int deleteDiningentertainmentByIds(Long[] ids)
    {
        return diningentertainmentMapper.deleteDiningentertainmentByIds(ids);
    }

    /**
     * 删除餐饮娱乐信息信息
     * 
     * @param id 餐饮娱乐信息主键
     * @return 结果
     */
    @Override
    public int deleteDiningentertainmentById(Long id)
    {
        return diningentertainmentMapper.deleteDiningentertainmentById(id);
    }
}
