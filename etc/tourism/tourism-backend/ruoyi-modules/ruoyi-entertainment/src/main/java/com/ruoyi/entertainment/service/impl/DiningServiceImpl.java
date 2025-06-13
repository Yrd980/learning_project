package com.ruoyi.entertainment.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.entertainment.mapper.DiningMapper;
import com.ruoyi.entertainment.domain.Dining;
import com.ruoyi.entertainment.service.IDiningService;

/**
 * 餐饮信息Service业务层处理
 * 
 * @author ningf
 * @date 2024-07-09
 */
@Service
public class DiningServiceImpl implements IDiningService 
{
    @Autowired
    private DiningMapper diningMapper;

    /**
     * 查询餐饮信息
     * 
     * @param id 餐饮信息主键
     * @return 餐饮信息
     */
    @Override
    public Dining selectDiningById(Long id)
    {
        return diningMapper.selectDiningById(id);
    }

    /**
     * 查询餐饮信息列表
     * 
     * @param dining 餐饮信息
     * @return 餐饮信息
     */
    @Override
    public List<Dining> selectDiningList(Dining dining)
    {
        return diningMapper.selectDiningList(dining);
    }

    /**
     * 新增餐饮信息
     * 
     * @param dining 餐饮信息
     * @return 结果
     */
    @Override
    public int insertDining(Dining dining)
    {
        return diningMapper.insertDining(dining);
    }

    /**
     * 修改餐饮信息
     * 
     * @param dining 餐饮信息
     * @return 结果
     */
    @Override
    public int updateDining(Dining dining)
    {
        return diningMapper.updateDining(dining);
    }

    /**
     * 批量删除餐饮信息
     * 
     * @param ids 需要删除的餐饮信息主键
     * @return 结果
     */
    @Override
    public int deleteDiningByIds(Long[] ids)
    {
        return diningMapper.deleteDiningByIds(ids);
    }

    /**
     * 删除餐饮信息信息
     * 
     * @param id 餐饮信息主键
     * @return 结果
     */
    @Override
    public int deleteDiningById(Long id)
    {
        return diningMapper.deleteDiningById(id);
    }
}
